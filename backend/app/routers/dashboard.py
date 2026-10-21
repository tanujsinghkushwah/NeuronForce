"""
Dashboard and Health API Router
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timezone

from app.database import get_db
from app.models import (
    Contact, Deal, Activity, AIAgentTask, AnalyticsSnapshot, DealStage
)
from app.schemas import DashboardStats

router = APIRouter(prefix="/api", tags=["Dashboard"])


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get comprehensive dashboard statistics."""
    total_contacts = db.query(Contact).count()
    total_deals = db.query(Deal).count()

    # Revenue from closed-won deals
    total_revenue = db.query(func.coalesce(func.sum(Deal.value), 0)).filter(
        Deal.stage == DealStage.CLOSED_WON
    ).scalar()

    # Pipeline value (active deals)
    pipeline_value = db.query(func.coalesce(func.sum(Deal.value), 0)).filter(
        Deal.stage.notin_([DealStage.CLOSED_WON, DealStage.CLOSED_LOST])
    ).scalar()

    deals_won = db.query(Deal).filter(Deal.stage == DealStage.CLOSED_WON).count()
    deals_lost = db.query(Deal).filter(Deal.stage == DealStage.CLOSED_LOST).count()
    active_deals = db.query(Deal).filter(
        Deal.stage.notin_([DealStage.CLOSED_WON, DealStage.CLOSED_LOST])
    ).count()

    total_closed = deals_won + deals_lost
    conversion_rate = (deals_won / total_closed * 100) if total_closed > 0 else 0
    avg_deal_size = (total_revenue / deals_won) if deals_won > 0 else 0

    # AI task stats for today
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0)
    ai_tasks_today = db.query(AIAgentTask).filter(AIAgentTask.created_at >= today_start).count()
    ai_cost_today = db.query(func.coalesce(func.sum(AIAgentTask.actual_cost), 0)).filter(
        AIAgentTask.created_at >= today_start
    ).scalar()

    # Revenue trend (last 30 days from analytics snapshots)
    snapshots = db.query(AnalyticsSnapshot).order_by(AnalyticsSnapshot.date).limit(30).all()
    revenue_trend = [
        {"date": s.date.isoformat(), "revenue": s.total_revenue, "pipeline": s.pipeline_value}
        for s in snapshots
    ]

    # Pipeline by stage
    pipeline_by_stage = []
    for stage in DealStage:
        stage_deals = db.query(Deal).filter(Deal.stage == stage).all()
        stage_value = sum(d.value or 0 for d in stage_deals)
        pipeline_by_stage.append({
            "stage": stage.value,
            "count": len(stage_deals),
            "value": stage_value,
        })

    # Top deals
    top_deals = db.query(Deal).filter(
        Deal.stage.notin_([DealStage.CLOSED_WON, DealStage.CLOSED_LOST])
    ).order_by(desc(Deal.value)).limit(5).all()
    top_deals_data = [
        {
            "id": d.id, "title": d.title, "value": d.value, "stage": d.stage.value,
            "company": d.company, "probability": d.probability
        }
        for d in top_deals
    ]

    # Recent activities
    recent = db.query(Activity).order_by(desc(Activity.created_at)).limit(10).all()
    recent_data = [
        {"id": a.id, "type": a.type.value, "subject": a.subject, "created_at": a.created_at.isoformat()}
        for a in recent
    ]

    # Lead sources
    sources = db.query(Contact.source, func.count(Contact.id)).group_by(Contact.source).all()
    lead_sources = [{"source": s[0] or "Unknown", "count": s[1]} for s in sources]

    return DashboardStats(
        total_contacts=total_contacts,
        total_deals=total_deals,
        total_revenue=total_revenue,
        pipeline_value=pipeline_value,
        conversion_rate=round(conversion_rate, 1),
        avg_deal_size=round(avg_deal_size, 2),
        deals_won=deals_won,
        deals_lost=deals_lost,
        active_deals=active_deals,
        ai_tasks_today=ai_tasks_today,
        ai_cost_today=round(ai_cost_today, 4),
        revenue_trend=revenue_trend,
        pipeline_by_stage=pipeline_by_stage,
        top_deals=top_deals_data,
        recent_activities=recent_data,
        lead_sources=lead_sources,
    )


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0", "timestamp": datetime.now(timezone.utc).isoformat()}
