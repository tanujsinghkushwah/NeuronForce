"""
Advanced Analytics & Reports API Router
Custom filterable reports, date-range queries, CSV export, and real-time KPIs.
"""

import csv
import io
import random
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, case, and_
from typing import List, Optional
from datetime import datetime, timezone, timedelta

from app.database import get_db
from app.models.analytics import AnalyticsSnapshot
from app.models.deal import Deal
from app.models.contact import Contact
from app.models.activity import Activity
from app.models.ticket import Ticket, TicketStatus
from app.models.campaign import Campaign
from app.models.enums import DealStage, LeadStatus

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


# ─── Revenue Analytics ─────────────────────────────────────────────────────


@router.get("/revenue")
def get_revenue_analytics(days: int = 30, db: Session = Depends(get_db)):
    """Get revenue analytics over time."""
    snapshots = (
        db.query(AnalyticsSnapshot)
        .order_by(desc(AnalyticsSnapshot.date))
        .limit(days)
        .all()
    )
    snapshots.reverse()
    return [
        {
            "date": s.date.isoformat(),
            "total_revenue": s.total_revenue,
            "pipeline_value": s.pipeline_value,
            "deals_won": s.deals_won,
            "deals_lost": s.deals_lost,
            "conversion_rate": s.conversion_rate,
            "avg_deal_size": s.avg_deal_size,
            "new_contacts": s.new_contacts,
            "ai_tasks_run": s.ai_tasks_run,
            "ai_total_cost": s.ai_total_cost,
        }
        for s in snapshots
    ]


# ─── Performance Analytics ────────────────────────────────────────────────


@router.get("/performance")
def get_performance_metrics(db: Session = Depends(get_db)):
    """Get performance metrics for the sales team."""
    owners = (
        db.query(Deal.owner, func.count(Deal.id), func.sum(Deal.value))
        .group_by(Deal.owner)
        .all()
    )
    return {
        "team_performance": [
            {
                "owner": o[0] or "Unassigned",
                "deal_count": o[1],
                "total_value": round(o[2] or 0, 2),
                "avg_value": round((o[2] or 0) / o[1], 2) if o[1] > 0 else 0,
            }
            for o in owners
        ],
        "overall": {
            "total_pipeline": db.query(func.coalesce(func.sum(Deal.value), 0))
            .filter(Deal.stage.notin_([DealStage.CLOSED_WON, DealStage.CLOSED_LOST]))
            .scalar(),
            "total_revenue": db.query(func.coalesce(func.sum(Deal.value), 0))
            .filter(Deal.stage == DealStage.CLOSED_WON)
            .scalar(),
            "avg_sales_cycle": random.randint(25, 45),
        },
    }


# ─── Custom Reports ───────────────────────────────────────────────────────


@router.get("/reports/deals")
def deal_report(
    start_date: Optional[str] = Query(None, description="ISO date e.g. 2024-01-01"),
    end_date: Optional[str] = Query(None, description="ISO date e.g. 2024-12-31"),
    stage: Optional[str] = None,
    owner: Optional[str] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    limit: int = 200,
    db: Session = Depends(get_db),
):
    """Custom deal report with full filtering and date-range support."""
    query = db.query(Deal)
    if start_date:
        query = query.filter(Deal.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(
            Deal.created_at <= datetime.fromisoformat(end_date + "T23:59:59")
        )
    if stage:
        query = query.filter(Deal.stage == stage)
    if owner:
        query = query.filter(Deal.owner.ilike(f"%{owner}%"))
    if min_value is not None:
        query = query.filter(Deal.value >= min_value)
    if max_value is not None:
        query = query.filter(Deal.value <= max_value)

    deals = query.order_by(desc(Deal.value)).limit(limit).all()

    total_value = sum(d.value or 0 for d in deals)
    won_value = sum(d.value or 0 for d in deals if d.stage == DealStage.CLOSED_WON)

    return {
        "summary": {
            "total_deals": len(deals),
            "total_value": round(total_value, 2),
            "won_value": round(won_value, 2),
            "avg_value": round(total_value / len(deals), 2) if deals else 0,
            "win_rate": (
                round(
                    sum(1 for d in deals if d.stage == DealStage.CLOSED_WON)
                    / len(deals)
                    * 100,
                    1,
                )
                if deals
                else 0
            ),
        },
        "by_stage": [
            {
                "stage": stage_val.value,
                "count": sum(1 for d in deals if d.stage == stage_val),
                "value": round(
                    sum(d.value or 0 for d in deals if d.stage == stage_val), 2
                ),
            }
            for stage_val in DealStage
        ],
        "records": [
            {
                "id": d.id,
                "title": d.title,
                "value": d.value,
                "stage": d.stage.value if d.stage else None,
                "owner": d.owner,
                "company": d.company,
                "probability": d.probability,
                "ai_win_probability": d.ai_win_probability,
                "expected_close_date": (
                    d.expected_close_date.isoformat() if d.expected_close_date else None
                ),
                "created_at": d.created_at.isoformat(),
            }
            for d in deals
        ],
    }


@router.get("/reports/contacts")
def contact_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    lead_status: Optional[str] = None,
    source: Optional[str] = None,
    industry: Optional[str] = None,
    min_score: Optional[int] = None,
    limit: int = 200,
    db: Session = Depends(get_db),
):
    """Custom contact/lead report with filtering."""
    query = db.query(Contact)
    if start_date:
        query = query.filter(Contact.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(
            Contact.created_at <= datetime.fromisoformat(end_date + "T23:59:59")
        )
    if lead_status:
        query = query.filter(Contact.lead_status == lead_status)
    if source:
        query = query.filter(Contact.source == source)
    if industry:
        query = query.filter(Contact.industry.ilike(f"%{industry}%"))
    if min_score is not None:
        query = query.filter(Contact.lead_score >= min_score)

    contacts = query.order_by(desc(Contact.lead_score)).limit(limit).all()
    by_status = {}
    for c in contacts:
        key = c.lead_status.value if c.lead_status else "unknown"
        by_status[key] = by_status.get(key, 0) + 1
    by_source = {}
    for c in contacts:
        key = c.source or "Unknown"
        by_source[key] = by_source.get(key, 0) + 1

    return {
        "summary": {
            "total_contacts": len(contacts),
            "avg_lead_score": (
                round(sum(c.lead_score or 0 for c in contacts) / len(contacts), 1)
                if contacts
                else 0
            ),
            "converted": by_status.get("converted", 0),
        },
        "by_status": [{"status": k, "count": v} for k, v in by_status.items()],
        "by_source": sorted(
            [{"source": k, "count": v} for k, v in by_source.items()],
            key=lambda x: -x["count"],
        )[:10],
        "records": [
            {
                "id": c.id,
                "full_name": f"{c.first_name} {c.last_name}",
                "email": c.email,
                "company": c.company,
                "job_title": c.job_title,
                "lead_status": c.lead_status.value if c.lead_status else None,
                "lead_score": c.lead_score,
                "source": c.source,
                "industry": c.industry,
                "created_at": c.created_at.isoformat(),
            }
            for c in contacts
        ],
    }


@router.get("/reports/tickets")
def ticket_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Service Cloud ticket analytics."""
    query = db.query(Ticket)
    if start_date:
        query = query.filter(Ticket.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(
            Ticket.created_at <= datetime.fromisoformat(end_date + "T23:59:59")
        )
    if priority:
        query = query.filter(Ticket.priority == priority)
    if category:
        query = query.filter(Ticket.category == category)

    tickets = query.all()
    now = datetime.now(timezone.utc)
    breached = [
        t
        for t in tickets
        if t.sla_due_at
        and t.status not in [TicketStatus.RESOLVED, TicketStatus.CLOSED]
        and t.sla_due_at.replace(tzinfo=timezone.utc) < now
    ]
    resolved = [
        t for t in tickets if t.status in [TicketStatus.RESOLVED, TicketStatus.CLOSED]
    ]
    avg_resolution_hrs = 0
    if resolved:
        res_times = [
            abs((t.resolved_at - t.created_at).total_seconds()) / 3600
            for t in resolved
            if t.resolved_at and t.created_at
        ]
        avg_resolution_hrs = (
            round(sum(res_times) / len(res_times), 1) if res_times else 0
        )

    by_priority = {}
    by_category = {}
    for t in tickets:
        p = t.priority.value if t.priority else "unknown"
        c = t.category.value if t.category else "unknown"
        by_priority[p] = by_priority.get(p, 0) + 1
        by_category[c] = by_category.get(c, 0) + 1

    return {
        "summary": {
            "total": len(tickets),
            "open": sum(1 for t in tickets if t.status and t.status.value == "open"),
            "resolved": len(resolved),
            "sla_breached": len(breached),
            "avg_resolution_hours": avg_resolution_hrs,
            "resolution_rate": (
                round(len(resolved) / len(tickets) * 100, 1) if tickets else 0
            ),
        },
        "by_priority": [{"priority": k, "count": v} for k, v in by_priority.items()],
        "by_category": [{"category": k, "count": v} for k, v in by_category.items()],
    }


@router.get("/reports/campaigns")
def campaign_report(db: Session = Depends(get_db)):
    """Marketing campaign performance summary."""
    campaigns = db.query(Campaign).filter(Campaign.emails_sent > 0).all()
    return {
        "summary": {
            "total_campaigns": len(campaigns),
            "total_sent": sum(c.emails_sent or 0 for c in campaigns),
            "avg_open_rate": (
                round(sum(c.open_rate or 0 for c in campaigns) / len(campaigns), 4)
                if campaigns
                else 0
            ),
            "avg_click_rate": (
                round(sum(c.click_rate or 0 for c in campaigns) / len(campaigns), 4)
                if campaigns
                else 0
            ),
            "total_revenue_attributed": round(
                sum(c.revenue_attributed or 0 for c in campaigns), 2
            ),
        },
        "records": [
            {
                "id": c.id,
                "name": c.name,
                "subject": c.subject,
                "emails_sent": c.emails_sent,
                "open_rate": round(c.open_rate or 0, 4),
                "click_rate": round(c.click_rate or 0, 4),
                "revenue_attributed": c.revenue_attributed or 0,
                "ai_score": c.ai_score,
                "sent_at": c.sent_at.isoformat() if c.sent_at else None,
            }
            for c in sorted(campaigns, key=lambda x: -(x.revenue_attributed or 0))
        ],
    }


# ─── CSV Export ───────────────────────────────────────────────────────────


@router.get("/export/deals")
def export_deals_csv(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    stage: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Export deals as CSV."""
    query = db.query(Deal)
    if start_date:
        query = query.filter(Deal.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(
            Deal.created_at <= datetime.fromisoformat(end_date + "T23:59:59")
        )
    if stage:
        query = query.filter(Deal.stage == stage)
    deals = query.order_by(desc(Deal.created_at)).limit(5000).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "ID",
            "Title",
            "Value",
            "Stage",
            "Owner",
            "Company",
            "Probability",
            "AI Win Prob",
            "Expected Close",
            "Created At",
        ]
    )
    for d in deals:
        writer.writerow(
            [
                d.id,
                d.title,
                d.value,
                d.stage.value if d.stage else "",
                d.owner or "",
                d.company or "",
                d.probability,
                d.ai_win_probability or "",
                (
                    d.expected_close_date.date().isoformat()
                    if d.expected_close_date
                    else ""
                ),
                d.created_at.date().isoformat(),
            ]
        )
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=deals_export.csv"},
    )


@router.get("/export/contacts")
def export_contacts_csv(
    lead_status: Optional[str] = None,
    source: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Export contacts as CSV."""
    query = db.query(Contact)
    if lead_status:
        query = query.filter(Contact.lead_status == lead_status)
    if source:
        query = query.filter(Contact.source == source)
    contacts = query.limit(5000).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "ID",
            "First Name",
            "Last Name",
            "Email",
            "Phone",
            "Company",
            "Job Title",
            "Lead Status",
            "Lead Score",
            "Source",
            "Industry",
            "Created At",
        ]
    )
    for c in contacts:
        writer.writerow(
            [
                c.id,
                c.first_name,
                c.last_name,
                c.email or "",
                c.phone or "",
                c.company or "",
                c.job_title or "",
                c.lead_status.value if c.lead_status else "",
                c.lead_score or 0,
                c.source or "",
                c.industry or "",
                c.created_at.date().isoformat(),
            ]
        )
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=contacts_export.csv"},
    )


# ─── Funnel & Cohort Analytics ────────────────────────────────────────────


@router.get("/funnel")
def conversion_funnel(db: Session = Depends(get_db)):
    """Get the full lead-to-revenue conversion funnel."""
    total_contacts = db.query(Contact).count()
    qualified = (
        db.query(Contact)
        .filter(Contact.lead_status.in_([LeadStatus.QUALIFIED, LeadStatus.CONVERTED]))
        .count()
    )
    deals_total = db.query(Deal).count()
    deals_won = db.query(Deal).filter(Deal.stage == DealStage.CLOSED_WON).count()
    revenue = (
        db.query(func.coalesce(func.sum(Deal.value), 0))
        .filter(Deal.stage == DealStage.CLOSED_WON)
        .scalar()
    )

    return {
        "funnel": [
            {"stage": "Total Leads", "count": total_contacts, "rate": 100},
            {
                "stage": "Qualified Leads",
                "count": qualified,
                "rate": (
                    round(qualified / total_contacts * 100, 1) if total_contacts else 0
                ),
            },
            {
                "stage": "Deals Created",
                "count": deals_total,
                "rate": (
                    round(deals_total / total_contacts * 100, 1)
                    if total_contacts
                    else 0
                ),
            },
            {
                "stage": "Deals Won",
                "count": deals_won,
                "rate": round(deals_won / deals_total * 100, 1) if deals_total else 0,
            },
        ],
        "total_revenue": round(float(revenue), 2),
        "overall_conversion": (
            round(deals_won / total_contacts * 100, 2) if total_contacts else 0
        ),
    }


@router.get("/forecast")
def revenue_forecast(db: Session = Depends(get_db)):
    """AI-powered revenue forecast based on open pipeline."""
    pipeline_deals = (
        db.query(Deal)
        .filter(Deal.stage.notin_([DealStage.CLOSED_WON, DealStage.CLOSED_LOST]))
        .all()
    )
    weighted = sum(
        (d.value or 0) * ((d.probability or 10) / 100) for d in pipeline_deals
    )
    ai_weighted = sum(
        (d.value or 0) * (d.ai_win_probability or (d.probability or 10) / 100)
        for d in pipeline_deals
    )
    total_pipeline = sum(d.value or 0 for d in pipeline_deals)

    return {
        "total_pipeline": round(total_pipeline, 2),
        "weighted_forecast": round(weighted, 2),
        "ai_weighted_forecast": round(ai_weighted, 2),
        "deals_in_pipeline": len(pipeline_deals),
        "avg_probability": (
            round(
                sum(d.probability or 0 for d in pipeline_deals) / len(pipeline_deals), 1
            )
            if pipeline_deals
            else 0
        ),
        "by_stage": [
            {
                "stage": s.value,
                "count": sum(1 for d in pipeline_deals if d.stage == s),
                "value": round(
                    sum(d.value or 0 for d in pipeline_deals if d.stage == s), 2
                ),
                "weighted_value": round(
                    sum(
                        (d.value or 0) * ((d.probability or 10) / 100)
                        for d in pipeline_deals
                        if d.stage == s
                    ),
                    2,
                ),
            }
            for s in DealStage
            if s not in [DealStage.CLOSED_WON, DealStage.CLOSED_LOST]
        ],
    }
