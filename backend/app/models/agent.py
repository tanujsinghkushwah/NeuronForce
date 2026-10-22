"""
AI Agent Telemetry and Task Models
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
from datetime import datetime, timezone

from app.database import Base
from app.models.enums import AgentTaskType, AgentTaskStatus


class AIAgentTask(Base):
    __tablename__ = "ai_agent_tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String(100), nullable=False)
    status = Column(SQLEnum(AgentTaskStatus), default=AgentTaskStatus.PENDING)
    input_data = Column(JSON, default=dict)
    output_data = Column(JSON, default=dict)
    confidence_score = Column(Float)
    cost_estimate = Column(Float)
    actual_cost = Column(Float)
    latency_ms = Column(Integer)
    error_message = Column(Text)
    triggered_by = Column(String(100))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime)
