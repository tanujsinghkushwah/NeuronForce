"""
NeuronForce Modular Data Models
Separated tables for Users, OAuth Accounts, Sessions, Contacts, Deals,
Activities, Agent Tasks, Analytics, and Calendar.
"""

from app.models.enums import (
    UserRole,
    LeadStatus,
    DealStage,
    Priority,
    TaskStatus,
    ActivityType,
    AgentTaskType,
    AgentTaskStatus,
)
from app.models.user import User
from app.models.oauth import OAuthAccount
from app.models.session import UserSession
from app.models.contact import Contact, deal_contacts
from app.models.deal import Deal
from app.models.activity import Activity, Task
from app.models.agent import AIAgentTask
from app.models.analytics import AnalyticsSnapshot
from app.models.calendar import CalendarEvent

__all__ = [
    "UserRole",
    "LeadStatus",
    "DealStage",
    "Priority",
    "TaskStatus",
    "ActivityType",
    "AgentTaskType",
    "AgentTaskStatus",
    "User",
    "OAuthAccount",
    "UserSession",
    "Contact",
    "deal_contacts",
    "Deal",
    "Activity",
    "Task",
    "AIAgentTask",
    "AnalyticsSnapshot",
    "CalendarEvent",
]
