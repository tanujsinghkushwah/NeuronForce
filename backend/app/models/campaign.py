"""
Email Campaign Data Models (Marketing Cloud)
"""

import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Enum as SQLEnum,
    JSON,
    Boolean,
    Float,
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base


class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CampaignType(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    NURTURE_SEQUENCE = "nurture_sequence"
    ANNOUNCEMENT = "announcement"
    PROMOTIONAL = "promotional"


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300), nullable=False)
    type = Column(SQLEnum(CampaignType), default=CampaignType.EMAIL)
    status = Column(SQLEnum(CampaignStatus), default=CampaignStatus.DRAFT, index=True)
    description = Column(Text)

    # Email content
    subject = Column(String(500))
    preview_text = Column(String(300))
    body_html = Column(Text)
    body_text = Column(Text)
    from_name = Column(String(200), default="NeuronForce Team")
    from_email = Column(String(255), default="noreply@neuronforce.ai")

    # Audience targeting
    audience_filter = Column(
        JSON, default=dict
    )  # e.g. {"industry": "SaaS", "lead_status": "qualified"}
    recipient_count = Column(Integer, default=0)

    # Scheduling
    scheduled_at = Column(DateTime)
    sent_at = Column(DateTime)
    completed_at = Column(DateTime)

    # Performance metrics
    emails_sent = Column(Integer, default=0)
    emails_delivered = Column(Integer, default=0)
    emails_opened = Column(Integer, default=0)
    emails_clicked = Column(Integer, default=0)
    emails_bounced = Column(Integer, default=0)
    emails_unsubscribed = Column(Integer, default=0)
    open_rate = Column(Float, default=0.0)
    click_rate = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)
    revenue_attributed = Column(Float, default=0.0)

    # AI optimization
    ai_score = Column(Integer)  # 0-100 campaign quality score
    ai_insights = Column(JSON, default=dict)
    ab_test_enabled = Column(Boolean, default=False)
    ab_variant_subject = Column(String(500))

    tags = Column(JSON, default=list)
    created_by = Column(String(200))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
