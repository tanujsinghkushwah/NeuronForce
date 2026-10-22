"""
Deal Model
Core revenue pipeline entity.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
    Enum as SQLEnum,
    JSON,
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base
from app.models.enums import DealStage, Priority
from app.models.contact import deal_contacts


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    value = Column(Float, default=0.0)
    currency = Column(String(3), default="USD")
    stage = Column(SQLEnum(DealStage), default=DealStage.PROSPECTING)
    probability = Column(Integer, default=10)
    expected_close_date = Column(DateTime)
    actual_close_date = Column(DateTime)
    description = Column(Text)
    company = Column(String(200))
    owner = Column(String(200))
    priority = Column(SQLEnum(Priority), default=Priority.MEDIUM)
    tags = Column(JSON, default=list)
    ai_win_probability = Column(Float)
    ai_insights = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    contacts = relationship("Contact", secondary=deal_contacts, back_populates="deals")
    activities = relationship(
        "Activity", back_populates="deal", cascade="all, delete-orphan"
    )
