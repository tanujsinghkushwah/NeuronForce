"""
AI Agents Telemetry and Execution API Router
Routes AI task execution through the centralized AI service (real OpenRouter inference or simulation fallback).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timezone
import time

from app.database import get_db
from app.models.agent import AIAgentTask
from app.models.enums import AgentTaskStatus
from app.schemas import (
    AIAgentTaskCreate,
    AIAgentTaskResponse,
    AIAgentChatRequest,
    AIAgentChatResponse
)
from app.services.ai_service import run_ai_task

router = APIRouter(prefix="/api/ai-agents", tags=["AI Agents"])


@router.get("/tasks", response_model=List[AIAgentTaskResponse])
def list_ai_tasks(
    skip: int = 0,
    limit: int = 20,
    task_type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List AI agent tasks with optional filtering."""
    query = db.query(AIAgentTask)
    if task_type:
        query = query.filter(AIAgentTask.task_type == task_type)
    if status:
        query = query.filter(AIAgentTask.status == status)
    return query.order_by(desc(AIAgentTask.created_at)).offset(skip).limit(limit).all()


@router.post("/tasks", response_model=AIAgentTaskResponse)
def create_ai_task(task: AIAgentTaskCreate, db: Session = Depends(get_db)):
    """Create and execute an AI agent task via OpenRouter (with simulation fallback)."""
    start_time = time.time()
    result = run_ai_task(task.task_type, task.input_data or {})
    elapsed_ms = int((time.time() - start_time) * 1000)

    db_task = AIAgentTask(
        task_type=task.task_type,
        status=AgentTaskStatus.COMPLETED,
        input_data=task.input_data or {},
        output_data=result["output"],
        confidence_score=result["confidence"],
        cost_estimate=result["cost"] * 1.1,
        actual_cost=result["cost"],
        latency_ms=result.get("latency_ms", elapsed_ms),
        triggered_by=task.triggered_by or "user",
        completed_at=datetime.now(timezone.utc),
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # Attach model metadata to response without breaking schema
    db_task.output_data = {
        **db_task.output_data,
        "_meta": {
            "model": result.get("model", "simulation"),
            "is_real_ai": result.get("is_real_ai", False),
        }
    }
    return db_task


@router.post("/chat", response_model=AIAgentChatResponse)
def execute_agent_chat(request: AIAgentChatRequest, db: Session = Depends(get_db)):
    """Execute autonomous LangGraph agent orchestrator from chat message."""
    import sys
    from pathlib import Path
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    from agents.orchestrator import run_agent_orchestrator

    start_time = time.time()
    result = run_agent_orchestrator(
        prompt=request.message,
        session_id=request.session_id or "default"
    )
    elapsed_ms = int((time.time() - start_time) * 1000)

    # Record in AIAgentTask table for telemetry & execution history
    try:
        task_type = result.get("target_subagent") or result.get("action_type") or "autonomous_chat"
        db_task = AIAgentTask(
            task_type=task_type,
            status=AgentTaskStatus.COMPLETED,
            input_data={"message": request.message, "session_id": request.session_id},
            output_data={
                "reply": result.get("reply"),
                "subagent_result": result.get("subagent_result"),
                "tool_result": result.get("tool_result"),
                "graph_steps_count": len(result.get("graph_steps", [])),
                "_meta": result.get("telemetry", {})
            },
            confidence_score=result.get("confidence_score", 0.92),
            cost_estimate=0.0004,
            actual_cost=result.get("telemetry", {}).get("cost", 0.0004),
            latency_ms=elapsed_ms,
            triggered_by="autonomous_chat",
            completed_at=datetime.now(timezone.utc),
        )
        db.add(db_task)
        db.commit()
    except Exception:
        db.rollback()

    return AIAgentChatResponse(**result)


@router.get("/stats")
def get_ai_stats(db: Session = Depends(get_db)):
    """Get AI agent performance and telemetry statistics."""
    total_tasks = db.query(AIAgentTask).count()
    completed = db.query(AIAgentTask).filter(AIAgentTask.status == AgentTaskStatus.COMPLETED).count()
    failed = db.query(AIAgentTask).filter(AIAgentTask.status == AgentTaskStatus.FAILED).count()
    running = db.query(AIAgentTask).filter(AIAgentTask.status == AgentTaskStatus.RUNNING).count()

    total_cost = db.query(func.coalesce(func.sum(AIAgentTask.actual_cost), 0)).scalar()
    avg_latency = db.query(func.coalesce(func.avg(AIAgentTask.latency_ms), 0)).filter(
        AIAgentTask.latency_ms.isnot(None)
    ).scalar()
    avg_confidence = db.query(func.coalesce(func.avg(AIAgentTask.confidence_score), 0)).filter(
        AIAgentTask.confidence_score.isnot(None)
    ).scalar()

    cost_by_type = db.query(
        AIAgentTask.task_type,
        func.sum(AIAgentTask.actual_cost),
        func.count(AIAgentTask.id),
        func.avg(AIAgentTask.latency_ms)
    ).group_by(AIAgentTask.task_type).all()

    from app.config import settings
    return {
        "total_tasks": total_tasks,
        "completed": completed,
        "failed": failed,
        "running": running,
        "success_rate": round(completed / total_tasks * 100, 1) if total_tasks > 0 else 0,
        "total_cost": round(total_cost, 4),
        "avg_latency_ms": round(avg_latency, 0),
        "avg_confidence": round(avg_confidence, 2),
        "ai_model": settings.OPENROUTER_MODEL,
        "real_ai_enabled": bool(settings.OPENROUTER_API_KEY),
        "cost_by_type": [
            {
                "type": c[0].value if hasattr(c[0], 'value') else c[0],
                "cost": round(c[1] or 0, 4),
                "count": c[2],
                "avg_latency": round(c[3] or 0, 0)
            }
            for c in cost_by_type
        ],
        "cost_efficiency": {
            "cost_per_task": round(total_cost / total_tasks, 4) if total_tasks > 0 else 0,
            "roi_estimate": round(total_cost * 150, 2),
            "time_saved_hours": round(total_tasks * 0.5, 1),
        }
    }
