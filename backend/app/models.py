"""
NeuronForce Data Models
Comprehensive SQLAlchemy models for the CRM platform.
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text,
    ForeignKey, Enum as SQLEnum, JSON, Table
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

from .database import Base


class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    UNQUALIFIED = "unqualified"
    CONVERTED = "converted"


class DealStage(str, enum.Enum):
    PROSPECTING = "prospecting"
    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ActivityType(str, enum.Enum):
    CALL = "call"
    EMAIL = "email"
    MEETING = "meeting"
    NOTE = "note"
    TASK = "task"


class AgentTaskType(str, enum.Enum):
    LEAD_SCORING = "lead_scoring"
    EMAIL_DRAFT = "email_draft"
    DEAL_ANALYSIS = "deal_analysis"
    CHURN_PREDICTION = "churn_prediction"
    MEETING_SUMMARY = "meeting_summary"
    FORECAST = "forecast"


class AgentTaskStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


# Association tables
deal_contacts = Table(
    'deal_contacts', Base.metadata,
    Column('deal_id', Integer, ForeignKey('deals.id'), primary_key=True),
    Column('contact_id', Integer, ForeignKey('contacts.id'), primary_key=True)
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
    lead_score = Column(Integer, default=0)  # 0-100 AI-computed score
    source = Column(String(100))  # e.g., "website", "referral", "linkedin"
    tags = Column(JSON, default=list)
    notes = Column(Text)
    last_contacted = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    deals = relationship("Deal", secondary=deal_contacts, back_populates="contacts")
    activities = relationship("Activity", back_populates="contact", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="contact", cascade="all, delete-orphan")


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    value = Column(Float, default=0.0)
    currency = Column(String(3), default="USD")
    stage = Column(SQLEnum(DealStage), default=DealStage.PROSPECTING)
    probability = Column(Integer, default=10)  # 0-100%
    expected_close_date = Column(DateTime)
    actual_close_date = Column(DateTime)
    description = Column(Text)
    company = Column(String(200))
    owner = Column(String(200))
    priority = Column(SQLEnum(Priority), default=Priority.MEDIUM)
    tags = Column(JSON, default=list)
    ai_win_probability = Column(Float)  # AI-predicted win probability
    ai_insights = Column(JSON, default=dict)  # AI-generated insights
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    contacts = relationship("Contact", secondary=deal_contacts, back_populates="deals")
    activities = relationship("Activity", back_populates="deal", cascade="all, delete-orphan")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(SQLEnum(ActivityType), nullable=False)
    subject = Column(String(300), nullable=False)
    description = Column(Text)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    deal_id = Column(Integer, ForeignKey("deals.id"))
    duration_minutes = Column(Integer)
    outcome = Column(String(200))
    scheduled_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    contact = relationship("Contact", back_populates="activities")
    deal = relationship("Deal", back_populates="activities")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO)
    priority = Column(SQLEnum(Priority), default=Priority.MEDIUM)
    due_date = Column(DateTime)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    assigned_to = Column(String(200))
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    contact = relationship("Contact", back_populates="tasks")


class AIAgentTask(Base):
    __tablename__ = "ai_agent_tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(SQLEnum(AgentTaskType), nullable=False)
    status = Column(SQLEnum(AgentTaskStatus), default=AgentTaskStatus.PENDING)
    input_data = Column(JSON, default=dict)
    output_data = Column(JSON, default=dict)
    confidence_score = Column(Float)
    cost_estimate = Column(Float)  # Estimated cost of AI operation
    actual_cost = Column(Float)  # Actual cost after execution
    latency_ms = Column(Integer)  # Execution time in milliseconds
    error_message = Column(Text)
    triggered_by = Column(String(100))  # "user", "automation", "schedule"
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime)


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


class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String(500))
    event_type = Column(String(50))  # "meeting", "call", "demo", "follow_up"
    attendees = Column(JSON, default=list)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    deal_id = Column(Integer, ForeignKey("deals.id"))
    color = Column(String(7))  # hex color for calendar display
    is_all_day = Column(Boolean, default=False)
    reminder_minutes = Column(Integer, default=15)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
