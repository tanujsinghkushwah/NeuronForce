"""
NeuronForce Pydantic Schemas
Request/Response models for the API.
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# --- Enums ---
class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    UNQUALIFIED = "unqualified"
    CONVERTED = "converted"


class DealStage(str, Enum):
    PROSPECTING = "prospecting"
    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# --- Contact Schemas ---
class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    avatar_url: Optional[str] = None
    lead_status: Optional[LeadStatus] = LeadStatus.NEW
    lead_score: Optional[int] = 0
    source: Optional[str] = None
    tags: Optional[List[str]] = []
    notes: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    industry: Optional[str] = None
    lead_status: Optional[LeadStatus] = None
    lead_score: Optional[int] = None
    source: Optional[str] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None


class ContactResponse(ContactBase):
    id: int
    last_contacted: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Deal Schemas ---
class DealBase(BaseModel):
    title: str
    value: Optional[float] = 0.0
    currency: Optional[str] = "USD"
    stage: Optional[DealStage] = DealStage.PROSPECTING
    probability: Optional[int] = 10
    expected_close_date: Optional[datetime] = None
    description: Optional[str] = None
    company: Optional[str] = None
    owner: Optional[str] = None
    priority: Optional[Priority] = Priority.MEDIUM
    tags: Optional[List[str]] = []


class DealCreate(DealBase):
    contact_ids: Optional[List[int]] = []


class DealUpdate(BaseModel):
    title: Optional[str] = None
    value: Optional[float] = None
    stage: Optional[DealStage] = None
    probability: Optional[int] = None
    expected_close_date: Optional[datetime] = None
    description: Optional[str] = None
    company: Optional[str] = None
    owner: Optional[str] = None
    priority: Optional[Priority] = None
    tags: Optional[List[str]] = None


class DealResponse(DealBase):
    id: int
    actual_close_date: Optional[datetime] = None
    ai_win_probability: Optional[float] = None
    ai_insights: Optional[Dict[str, Any]] = {}
    contacts: Optional[List[ContactResponse]] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Activity Schemas ---
class ActivityBase(BaseModel):
    type: str
    subject: str
    description: Optional[str] = None
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None
    duration_minutes: Optional[int] = None
    outcome: Optional[str] = None
    scheduled_at: Optional[datetime] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityResponse(ActivityBase):
    id: int
    completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Task Schemas ---
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.TODO
    priority: Optional[Priority] = Priority.MEDIUM
    due_date: Optional[datetime] = None
    contact_id: Optional[int] = None
    assigned_to: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- AI Agent Schemas ---
class AIAgentTaskCreate(BaseModel):
    task_type: str
    input_data: Optional[Dict[str, Any]] = {}
    triggered_by: Optional[str] = "user"


class AIAgentTaskResponse(BaseModel):
    id: int
    task_type: str
    status: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    confidence_score: Optional[float] = None
    cost_estimate: Optional[float] = None
    actual_cost: Optional[float] = None
    latency_ms: Optional[int] = None
    error_message: Optional[str] = None
    triggered_by: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class AIAgentChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    context: Optional[Dict[str, Any]] = None


class AIAgentChatResponse(BaseModel):
    reply: str
    intent: Optional[str] = None
    target_subagent: Optional[str] = None
    action_type: Optional[str] = None
    subagent_result: Optional[Dict[str, Any]] = None
    tool_result: Optional[Dict[str, Any]] = None
    graph_steps: List[Dict[str, Any]] = []
    telemetry: Dict[str, Any] = {}
    confidence_score: float = 0.92


# --- Calendar Schemas ---
class CalendarEventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    event_type: Optional[str] = "meeting"
    attendees: Optional[List[str]] = []
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None
    color: Optional[str] = "#6366f1"
    is_all_day: Optional[bool] = False
    reminder_minutes: Optional[int] = 15


class CalendarEventCreate(CalendarEventBase):
    pass


class CalendarEventResponse(CalendarEventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Analytics Schemas ---
class DashboardStats(BaseModel):
    total_contacts: int
    total_deals: int
    total_revenue: float
    pipeline_value: float
    conversion_rate: float
    avg_deal_size: float
    deals_won: int
    deals_lost: int
    active_deals: int
    ai_tasks_today: int
    ai_cost_today: float
    revenue_trend: List[Dict[str, Any]]
    pipeline_by_stage: List[Dict[str, Any]]
    top_deals: List[Dict[str, Any]]
    recent_activities: List[Dict[str, Any]]
    lead_sources: List[Dict[str, Any]]


class PipelineView(BaseModel):
    stages: Dict[str, List[DealResponse]]
    total_value: float
    weighted_value: float


# --- Auth & User Schemas ---
class UserBase(BaseModel):
    email: str
    full_name: str
    avatar_url: Optional[str] = None
    role: Optional[str] = "sales_rep"


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GoogleAuthRequest(BaseModel):
    credential: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    sub: Optional[str] = None
    role: Optional[str] = "sales_rep"


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class SessionResponse(BaseModel):
    id: int
    user_id: int
    session_token: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    expires_at: datetime
    is_revoked: bool
    created_at: datetime
    last_active_at: datetime

    model_config = ConfigDict(from_attributes=True)
