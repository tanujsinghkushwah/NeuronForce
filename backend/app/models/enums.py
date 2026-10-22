"""
NeuronForce Core Model Enums
"""

import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    REVOPS_LEAD = "revops_lead"
    SALES_REP = "sales_rep"
    VIEWER = "viewer"


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
    DEAL_RISK = "deal_risk"
    CHURN_PREDICTION = "churn_prediction"
    MEETING_SUMMARY = "meeting_summary"
    FORECAST = "forecast"
    AUTONOMOUS_CHAT = "autonomous_chat"
    SCHEDULE_MEETING = "schedule_meeting"
    CREATE_DEAL = "create_deal"
    UPDATE_DEAL = "update_deal"
    CREATE_CONTACT = "create_contact"
    UPDATE_CONTACT = "update_contact"
    CREATE_CAMPAIGN = "create_campaign"


class AgentTaskStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
