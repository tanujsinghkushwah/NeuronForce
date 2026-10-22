"""
Contact Data Model & Association Tables
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    Enum as SQLEnum,
    JSON,
    Table,
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base
from app.models.enums import LeadStatus

# Association table between deals and contacts
deal_contacts = Table(
    "deal_contacts",
    Base.metadata,
    Column("deal_id", Integer, ForeignKey("deals.id"), primary_key=True),
    Column("contact_id", Integer, ForeignKey("contacts.id"), primary_key=True),
)


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(50))
    company = Column(String(200))
    job_title = Column(String(200))
    department = Column(String(100))
    industry = Column(String(100))
    website = Column(String(500))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    avatar_url = Column(String(500))
    lead_status = Column(SQLEnum(LeadStatus), default=LeadStatus.NEW)
    lead_score = Column(Integer, default=0)
    source = Column(String(100))
    tags = Column(JSON, default=list)
    notes = Column(Text)
    last_contacted = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    deals = relationship("Deal", secondary=deal_contacts, back_populates="contacts")
    activities = relationship(
        "Activity", back_populates="contact", cascade="all, delete-orphan"
    )
    tasks = relationship("Task", back_populates="contact", cascade="all, delete-orphan")
