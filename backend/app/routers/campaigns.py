"""
Email Campaign Management API Router (Marketing Cloud)
"""

import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel

from app.database import get_db
from app.models.campaign import Campaign, CampaignStatus, CampaignType
from app.models.contact import Contact
from app.services.ai_service import run_ai_task

router = APIRouter(prefix="/api/campaigns", tags=["Campaigns"])


# ─── Pydantic schemas ───────────────────────────────────────────────────────


class CampaignCreate(BaseModel):
    name: str
    type: Optional[str] = "email"
    description: Optional[str] = None
    subject: Optional[str] = None
    preview_text: Optional[str] = None
    body_html: Optional[str] = None
    body_text: Optional[str] = None
    from_name: Optional[str] = "NeuronForce Team"
    from_email: Optional[str] = "noreply@neuronforce.ai"
    audience_filter: Optional[dict] = {}
    scheduled_at: Optional[datetime] = None
    ab_test_enabled: Optional[bool] = False
    ab_variant_subject: Optional[str] = None
    tags: Optional[List[str]] = []


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    subject: Optional[str] = None
    preview_text: Optional[str] = None
    body_html: Optional[str] = None
    body_text: Optional[str] = None
    audience_filter: Optional[dict] = None
    scheduled_at: Optional[datetime] = None
    tags: Optional[List[str]] = None


# ─── Helpers ───────────────────────────────────────────────────────────────


def _compute_recipient_count(db: Session, audience_filter: dict) -> int:
    """Estimate recipient count from audience filter criteria."""
    query = db.query(Contact)
    if industry := audience_filter.get("industry"):
        query = query.filter(Contact.industry == industry)
    if lead_status := audience_filter.get("lead_status"):
        query = query.filter(Contact.lead_status == lead_status)
    if source := audience_filter.get("source"):
        query = query.filter(Contact.source == source)
    return query.count()


def _simulate_send_metrics(recipient_count: int) -> dict:
    """Generate realistic send metrics for demonstration."""
    delivered = int(recipient_count * random.uniform(0.95, 0.99))
    opened = int(delivered * random.uniform(0.20, 0.45))
    clicked = int(opened * random.uniform(0.10, 0.30))
    bounced = recipient_count - delivered
    unsubs = int(delivered * random.uniform(0.002, 0.01))
    return {
        "emails_sent": recipient_count,
        "emails_delivered": delivered,
        "emails_opened": opened,
        "emails_clicked": clicked,
        "emails_bounced": bounced,
        "emails_unsubscribed": unsubs,
        "open_rate": round(opened / delivered, 4) if delivered > 0 else 0,
        "click_rate": round(clicked / delivered, 4) if delivered > 0 else 0,
        "revenue_attributed": round(clicked * random.uniform(80, 400), 2),
    }


def _campaign_to_dict(c: Campaign) -> dict:
    return {
        "id": c.id,
        "name": c.name,
        "type": c.type.value if c.type else "email",
        "status": c.status.value if c.status else "draft",
        "description": c.description,
        "subject": c.subject,
        "preview_text": c.preview_text,
        "body_html": c.body_html,
        "body_text": c.body_text,
        "from_name": c.from_name,
        "from_email": c.from_email,
        "audience_filter": c.audience_filter or {},
        "recipient_count": c.recipient_count,
        "scheduled_at": c.scheduled_at.isoformat() if c.scheduled_at else None,
        "sent_at": c.sent_at.isoformat() if c.sent_at else None,
        "completed_at": c.completed_at.isoformat() if c.completed_at else None,
        "emails_sent": c.emails_sent,
        "emails_delivered": c.emails_delivered,
        "emails_opened": c.emails_opened,
        "emails_clicked": c.emails_clicked,
        "emails_bounced": c.emails_bounced,
        "emails_unsubscribed": c.emails_unsubscribed,
        "open_rate": c.open_rate,
        "click_rate": c.click_rate,
        "conversion_rate": c.conversion_rate,
        "revenue_attributed": c.revenue_attributed,
        "ai_score": c.ai_score,
        "ai_insights": c.ai_insights or {},
        "ab_test_enabled": c.ab_test_enabled,
        "ab_variant_subject": c.ab_variant_subject,
        "tags": c.tags or [],
        "created_by": c.created_by,
        "created_at": c.created_at.isoformat(),
        "updated_at": c.updated_at.isoformat(),
    }


# ─── Routes ────────────────────────────────────────────────────────────────


@router.get("")
def list_campaigns(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Campaign)
    if status:
        query = query.filter(Campaign.status == status)
    campaigns = (
        query.order_by(desc(Campaign.created_at)).offset(skip).limit(limit).all()
    )
    return [_campaign_to_dict(c) for c in campaigns]


@router.post("")
def create_campaign(payload: CampaignCreate, db: Session = Depends(get_db)):
    """Create a new campaign with optional AI analysis."""
    recipient_count = _compute_recipient_count(db, payload.audience_filter or {})

    campaign = Campaign(
        name=payload.name,
        type=payload.type,
        description=payload.description,
        subject=payload.subject,
        preview_text=payload.preview_text,
        body_html=payload.body_html,
        body_text=payload.body_text,
        from_name=payload.from_name,
        from_email=payload.from_email,
        audience_filter=payload.audience_filter or {},
        recipient_count=recipient_count,
        scheduled_at=payload.scheduled_at,
        ab_test_enabled=payload.ab_test_enabled,
        ab_variant_subject=payload.ab_variant_subject,
        tags=payload.tags or [],
    )

    # Run AI optimization analysis if subject line is provided
    if payload.subject:
        ai_result = run_ai_task(
            "campaign_optimize",
            {
                "subject": payload.subject,
                "preview_text": payload.preview_text,
                "campaign_type": payload.type,
                "audience_filter": payload.audience_filter,
                "recipient_count": recipient_count,
            },
        )
        output = ai_result["output"]
        campaign.ai_score = output.get("subject_line_score", 70)
        campaign.ai_insights = {
            "predicted_open_rate": output.get("predicted_open_rate"),
            "predicted_click_rate": output.get("predicted_click_rate"),
            "improvements": output.get("improvements", []),
            "optimal_send_time": output.get("optimal_send_time"),
            "ab_test_suggestion": output.get("ab_test_suggestion"),
            "audience_fit_score": output.get("audience_fit_score"),
            "is_real_ai": ai_result.get("is_real_ai", False),
        }

    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return _campaign_to_dict(campaign)


@router.get("/templates")
def list_campaign_templates():
    """Pre-built high-converting email campaign templates."""
    return [
        {
            "id": "enterprise_webinar",
            "name": "Enterprise C-Level Webinar Invite",
            "type": "email",
            "subject": "Exclusive Invite: Scaling Revenue Operations with Autonomous AI Agents",
            "preview_text": "Join 500+ RevOps executives for live pipeline automation benchmarks.",
            "body_html": "<p>Hi {{first_name}},</p><p>Enterprise sales teams are eliminating 80% of manual CRM data entry using autonomous agents.</p><p><a href='#'>Register for the live briefing &rarr;</a></p>",
            "body_text": "Hi {{first_name}},\n\nEnterprise sales teams are eliminating 80% of manual CRM data entry using autonomous agents.\n\nRegister for the live briefing: https://neuronforce.ai/webinar-q4",
            "suggested_audience": {
                "industry": "Technology",
                "lead_status": "qualified",
            },
        },
        {
            "id": "closed_lost_nurture",
            "name": "Closed-Lost Re-engagement Nurture",
            "type": "nurture_sequence",
            "subject": "What's new in NeuronForce 2.0: Real-time autonomous pipeline intelligence",
            "preview_text": "See how our new release addresses integration bottlenecks.",
            "body_html": "<p>Hi {{first_name}},</p><p>We recently shipped our Gemini-powered Agentforce layer with automatic SLA triaging and 1-click quoting.</p>",
            "body_text": "Hi {{first_name}},\n\nWe recently shipped our Gemini-powered Agentforce layer with automatic SLA triaging and 1-click quoting.",
            "suggested_audience": {"lead_status": "contacted"},
        },
        {
            "id": "product_launch",
            "name": "Product Launch Announcement",
            "type": "announcement",
            "subject": "Announcing NeuronForce Agentforce: AI that doesn't just suggest — it executes",
            "preview_text": "Next-generation autonomous revenue orchestration is now live.",
            "body_html": "<p>Meet Agentforce: The first AI sales platform with real-time Gemini reasoning.</p>",
            "body_text": "Meet Agentforce: The first AI sales platform with real-time Gemini reasoning.",
            "suggested_audience": {},
        },
        {
            "id": "promotional_discount",
            "name": "Annual Upgrade Discount Incentive",
            "type": "promotional",
            "subject": "Upgrade your team's pipeline velocity: Save 20% on Annual Pro",
            "preview_text": "Lock in your 2026 pricing and unlock unlimited AI agent tasks.",
            "body_html": "<p>Hi {{first_name}},</p><p>Switch to Annual Pro today and get unlimited Agentforce execution.</p>",
            "body_text": "Hi {{first_name}},\n\nSwitch to Annual Pro today and get unlimited Agentforce execution.",
            "suggested_audience": {"industry": "Finance"},
        },
    ]


@router.get("/stats")
def campaign_stats(db: Session = Depends(get_db)):
    """Get Marketing Cloud KPIs."""
    total = db.query(Campaign).count()
    active = db.query(Campaign).filter(Campaign.status == CampaignStatus.ACTIVE).count()
    completed = (
        db.query(Campaign).filter(Campaign.status == CampaignStatus.COMPLETED).count()
    )
    draft = db.query(Campaign).filter(Campaign.status == CampaignStatus.DRAFT).count()
    total_sent = db.query(func.coalesce(func.sum(Campaign.emails_sent), 0)).scalar()
    total_revenue = db.query(
        func.coalesce(func.sum(Campaign.revenue_attributed), 0)
    ).scalar()
    avg_open_rate = (
        db.query(func.coalesce(func.avg(Campaign.open_rate), 0))
        .filter(Campaign.emails_sent > 0)
        .scalar()
    )
    avg_click_rate = (
        db.query(func.coalesce(func.avg(Campaign.click_rate), 0))
        .filter(Campaign.emails_sent > 0)
        .scalar()
    )

    return {
        "total": total,
        "total_campaigns": total,
        "active": active,
        "active_campaigns": active,
        "completed": completed,
        "completed_campaigns": completed,
        "draft": draft,
        "total_emails_sent": int(total_sent),
        "total_revenue_attributed": round(float(total_revenue), 2),
        "avg_open_rate": round(float(avg_open_rate), 4),
        "avg_click_rate": round(float(avg_click_rate), 4),
    }


@router.get("/{campaign_id}")
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    c = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return _campaign_to_dict(c)


@router.put("/{campaign_id}")
def update_campaign(
    campaign_id: int, payload: CampaignUpdate, db: Session = Depends(get_db)
):
    c = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Campaign not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        if field == "audience_filter" and value is not None:
            c.recipient_count = _compute_recipient_count(db, value)
        setattr(c, field, value)
    db.commit()
    db.refresh(c)
    return _campaign_to_dict(c)


@router.post("/{campaign_id}/send")
def send_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Simulate sending a campaign and record metrics."""
    c = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if c.status not in [CampaignStatus.DRAFT, CampaignStatus.SCHEDULED]:
        raise HTTPException(
            status_code=400, detail=f"Cannot send campaign in status: {c.status.value}"
        )
    if not c.recipient_count:
        c.recipient_count = _compute_recipient_count(db, c.audience_filter or {})
        if not c.recipient_count:
            c.recipient_count = random.randint(50, 500)  # demo fallback

    metrics = _simulate_send_metrics(c.recipient_count)
    for k, v in metrics.items():
        setattr(c, k, v)
    c.status = CampaignStatus.COMPLETED
    c.sent_at = datetime.now(timezone.utc)
    c.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(c)
    return _campaign_to_dict(c)


@router.post("/{campaign_id}/ai-optimize")
def ai_optimize_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Run AI optimization analysis on an existing campaign."""
    c = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Campaign not found")

    result = run_ai_task(
        "campaign_optimize",
        {
            "subject": c.subject,
            "preview_text": c.preview_text,
            "body_text": (c.body_text or "")[:500],
            "current_open_rate": c.open_rate,
            "current_click_rate": c.click_rate,
            "recipient_count": c.recipient_count,
        },
    )
    output = result["output"]
    c.ai_score = output.get("subject_line_score", c.ai_score or 70)
    c.ai_insights = {
        **(c.ai_insights or {}),
        **{
            "predicted_open_rate": output.get("predicted_open_rate"),
            "improvements": output.get("improvements", []),
            "optimal_send_time": output.get("optimal_send_time"),
            "ab_test_suggestion": output.get("ab_test_suggestion"),
            "is_real_ai": result.get("is_real_ai", False),
        },
    }
    db.commit()
    return {"ai_score": c.ai_score, "ai_insights": c.ai_insights}


@router.delete("/{campaign_id}")
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    c = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Campaign not found")
    db.delete(c)
    db.commit()
    return {"message": f"Campaign {campaign_id} deleted"}
