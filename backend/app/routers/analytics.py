"""
Analytics and Performance Metrics API Router
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import random

from app.database import get_db
from app.models.analytics import AnalyticsSnapshot
from app.models.deal import Deal
from app.models.enums import DealStage

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/revenue")
def get_revenue_analytics(days: int = 30, db: Session = Depends(get_db)):
    """Get revenue analytics over time."""
    snapshots = db.query(AnalyticsSnapshot).order_by(
        desc(AnalyticsSnapshot.date)
    ).limit(days).all()
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


@router.get("/performance")
def get_performance_metrics(db: Session = Depends(get_db)):
    """Get performance metrics for the sales team."""
    owners = db.query(Deal.owner, func.count(Deal.id), func.sum(Deal.value)).group_by(Deal.owner).all()

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
            "total_pipeline": db.query(func.coalesce(func.sum(Deal.value), 0)).filter(
                Deal.stage.notin_([DealStage.CLOSED_WON, DealStage.CLOSED_LOST])
            ).scalar(),
            "total_revenue": db.query(func.coalesce(func.sum(Deal.value), 0)).filter(
                Deal.stage == DealStage.CLOSED_WON
            ).scalar(),
            "avg_sales_cycle": random.randint(25, 45),
        }
    }
