"""
Analytics Snapshot Model
"""

from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime, timezone

from app.database import Base


class AnalyticsSnapshot(Base):
    __tablename__ = "analytics_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    total_revenue = Column(Float, default=0.0)
    deals_won = Column(Integer, default=0)
    deals_lost = Column(Integer, default=0)
    new_contacts = Column(Integer, default=0)
    active_deals = Column(Integer, default=0)
    pipeline_value = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)
    avg_deal_size = Column(Float, default=0.0)
    ai_tasks_run = Column(Integer, default=0)
    ai_total_cost = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
