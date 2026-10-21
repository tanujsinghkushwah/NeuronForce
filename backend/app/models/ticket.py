"""
Support Ticket & Case Data Models (Service Cloud)
"""

import enum
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SQLEnum, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base


class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PENDING_CUSTOMER = "pending_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TicketCategory(str, enum.Enum):
    BUG = "bug"
    BILLING = "billing"
    FEATURE_REQUEST = "feature_request"
    TECHNICAL = "technical"
    GENERAL = "general"
    ONBOARDING = "onboarding"


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(20), unique=True, index=True)  # e.g. TKT-0001
    title = Column(String(300), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(TicketStatus), default=TicketStatus.OPEN, index=True)
    priority = Column(SQLEnum(TicketPriority), default=TicketPriority.MEDIUM, index=True)
    category = Column(SQLEnum(TicketCategory), default=TicketCategory.GENERAL)

    # Relationships to CRM entities
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=True)

    # Assignment
    assigned_to = Column(String(200))
    reporter_email = Column(String(255))
    reporter_name = Column(String(200))

    # SLA tracking
    sla_due_at = Column(DateTime)
    first_response_at = Column(DateTime)
    resolved_at = Column(DateTime)

    # AI analysis
    ai_triage = Column(JSON, default=dict)
    sentiment = Column(String(50))
    ai_suggested_response = Column(Text)

    tags = Column(JSON, default=list)
    internal_notes = Column(Text)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    messages = relationship("TicketMessage", back_populates="ticket", cascade="all, delete-orphan", order_by="TicketMessage.created_at")


class TicketMessage(Base):
    __tablename__ = "ticket_messages"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False)
    author_name = Column(String(200), nullable=False)
    author_email = Column(String(255))
    body = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=False)  # internal agent notes vs customer-visible
    is_ai_generated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    ticket = relationship("Ticket", back_populates="messages")
