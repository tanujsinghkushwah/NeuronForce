"""
Support Tickets & Cases API Router (Service Cloud)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel

from app.database import get_db
from app.models.ticket import Ticket, TicketMessage, TicketStatus, TicketPriority, TicketCategory
from app.services.ai_service import run_ai_task

router = APIRouter(prefix="/api/tickets", tags=["Tickets"])

SLA_HOURS = {
    TicketPriority.CRITICAL: 1,
    TicketPriority.HIGH: 4,
    TicketPriority.MEDIUM: 24,
    TicketPriority.LOW: 72,
}


# ─── Pydantic schemas ───────────────────────────────────────────────────────

class TicketCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    category: Optional[str] = "general"
    reporter_name: Optional[str] = None
    reporter_email: Optional[str] = None
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None
    tags: Optional[List[str]] = []
    ai_triage: Optional[bool] = True


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    assigned_to: Optional[str] = None
    internal_notes: Optional[str] = None
    tags: Optional[List[str]] = None


class MessageCreate(BaseModel):
    body: str
    author_name: str
    author_email: Optional[str] = None
    is_internal: Optional[bool] = False


# ─── Helpers ───────────────────────────────────────────────────────────────

def _generate_ticket_number(db: Session) -> str:
    count = db.query(func.count(Ticket.id)).scalar()
    return f"TKT-{count + 1:04d}"


def _sla_due(priority: str) -> datetime:
    hours = SLA_HOURS.get(TicketPriority(priority), 24)
    return datetime.now(timezone.utc) + timedelta(hours=hours)


def _ticket_to_dict(t: Ticket) -> dict:
    now = datetime.now(timezone.utc)
    sla_breached = t.sla_due_at and t.status not in [TicketStatus.RESOLVED, TicketStatus.CLOSED] and t.sla_due_at.replace(tzinfo=timezone.utc) < now
    return {
        "id": t.id,
        "ticket_number": t.ticket_number,
        "title": t.title,
        "description": t.description,
        "status": t.status.value if t.status else "open",
        "priority": t.priority.value if t.priority else "medium",
        "category": t.category.value if t.category else "general",
        "assigned_to": t.assigned_to,
        "reporter_name": t.reporter_name,
        "reporter_email": t.reporter_email,
        "contact_id": t.contact_id,
        "deal_id": t.deal_id,
        "sla_due_at": t.sla_due_at.isoformat() if t.sla_due_at else None,
        "sla_breached": bool(sla_breached),
        "first_response_at": t.first_response_at.isoformat() if t.first_response_at else None,
        "resolved_at": t.resolved_at.isoformat() if t.resolved_at else None,
        "ai_triage": t.ai_triage or {},
        "sentiment": t.sentiment,
        "ai_suggested_response": t.ai_suggested_response,
        "tags": t.tags or [],
        "internal_notes": t.internal_notes,
        "messages": [
            {
                "id": m.id,
                "author_name": m.author_name,
                "author_email": m.author_email,
                "body": m.body,
                "is_internal": m.is_internal,
                "is_ai_generated": m.is_ai_generated,
                "created_at": m.created_at.isoformat(),
            }
            for m in (t.messages or [])
        ],
        "created_at": t.created_at.isoformat(),
        "updated_at": t.updated_at.isoformat(),
    }


# ─── Routes ────────────────────────────────────────────────────────────────

@router.get("")
def list_tickets(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List tickets with filtering."""
    query = db.query(Ticket)
    if status:
        query = query.filter(Ticket.status == status)
    if priority:
        query = query.filter(Ticket.priority == priority)
    if category:
        query = query.filter(Ticket.category == category)
    if search:
        query = query.filter(
            Ticket.title.ilike(f"%{search}%") | Ticket.description.ilike(f"%{search}%")
        )
    tickets = query.order_by(desc(Ticket.created_at)).offset(skip).limit(limit).all()
    return [_ticket_to_dict(t) for t in tickets]


@router.post("")
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    """Create a new support ticket with optional AI triage."""
    ticket = Ticket(
        ticket_number=_generate_ticket_number(db),
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        category=payload.category,
        reporter_name=payload.reporter_name,
        reporter_email=payload.reporter_email,
        contact_id=payload.contact_id,
        deal_id=payload.deal_id,
        tags=payload.tags or [],
        sla_due_at=_sla_due(payload.priority or "medium"),
    )

    # Run AI triage if requested
    if payload.ai_triage:
        result = run_ai_task("ticket_triage", {
            "title": payload.title,
            "description": payload.description,
            "category": payload.category,
            "priority": payload.priority,
            "reporter": payload.reporter_name,
        })
        output = result["output"]
        ticket.ai_triage = output
        ticket.sentiment = output.get("sentiment", "neutral")
        ticket.ai_suggested_response = output.get("suggested_response")
        # Override priority if AI recommends escalation
        if output.get("escalate") and payload.priority in ("low", "medium"):
            ticket.priority = "high"

    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return _ticket_to_dict(ticket)


@router.get("/stats")
def ticket_stats(db: Session = Depends(get_db)):
    """Get Service Cloud KPIs."""
    total = db.query(Ticket).count()
    open_count = db.query(Ticket).filter(Ticket.status == TicketStatus.OPEN).count()
    in_progress = db.query(Ticket).filter(Ticket.status == TicketStatus.IN_PROGRESS).count()
    resolved = db.query(Ticket).filter(Ticket.status == TicketStatus.RESOLVED).count()
    critical = db.query(Ticket).filter(Ticket.priority == TicketPriority.CRITICAL).count()

    now = datetime.now(timezone.utc)
    sla_breached = db.query(Ticket).filter(
        Ticket.sla_due_at < now,
        Ticket.status.notin_([TicketStatus.RESOLVED, TicketStatus.CLOSED])
    ).count()

    by_category = db.query(Ticket.category, func.count(Ticket.id)).group_by(Ticket.category).all()
    by_priority = db.query(Ticket.priority, func.count(Ticket.id)).group_by(Ticket.priority).all()

    return {
        "total": total,
        "total_tickets": total,
        "open": open_count,
        "open_tickets": open_count,
        "in_progress": in_progress,
        "in_progress_tickets": in_progress,
        "resolved": resolved,
        "resolved_tickets": resolved,
        "critical": critical,
        "sla_breached": sla_breached,
        "resolution_rate": round(resolved / total * 100, 1) if total > 0 else 0,
        "by_category": [{"category": c[0].value if hasattr(c[0], "value") else c[0], "count": c[1]} for c in by_category],
        "by_priority": [{"priority": p[0].value if hasattr(p[0], "value") else p[0], "count": p[1]} for p in by_priority],
    }


@router.get("/{ticket_id}")
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    t = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return _ticket_to_dict(t)


@router.put("/{ticket_id}")
@router.patch("/{ticket_id}")
def update_ticket(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)):
    t = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(t, field, value)
    if payload.status in ("resolved", "closed") and not t.resolved_at:
        t.resolved_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(t)
    return _ticket_to_dict(t)


@router.post("/{ticket_id}/messages")
def add_message(ticket_id: int, payload: MessageCreate, db: Session = Depends(get_db)):
    """Add a message (reply) to a ticket."""
    t = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")

    msg = TicketMessage(
        ticket_id=ticket_id,
        author_name=payload.author_name,
        author_email=payload.author_email,
        body=payload.body,
        is_internal=payload.is_internal,
    )
    db.add(msg)

    # Mark first response time
    if not t.first_response_at and not payload.is_internal:
        t.first_response_at = datetime.now(timezone.utc)
    if t.status == TicketStatus.OPEN and not payload.is_internal:
        t.status = TicketStatus.IN_PROGRESS

    db.commit()
    db.refresh(msg)
    return {"id": msg.id, "body": msg.body, "author_name": msg.author_name, "created_at": msg.created_at.isoformat()}


@router.post("/{ticket_id}/ai-reply")
def generate_ai_reply(ticket_id: int, db: Session = Depends(get_db)):
    """Generate an AI-suggested reply for a ticket."""
    t = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")

    result = run_ai_task("ticket_triage", {
        "title": t.title,
        "description": t.description,
        "category": t.category.value if t.category else "general",
        "priority": t.priority.value if t.priority else "medium",
        "messages_count": len(t.messages),
    })
    suggested = result["output"].get("suggested_response", "Thank you for contacting support. We are reviewing your request.")
    t.ai_suggested_response = suggested
    db.commit()
    return {"suggested_response": suggested, "is_real_ai": result.get("is_real_ai", False)}


@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    t = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db.delete(t)
    db.commit()
    return {"message": f"Ticket {ticket_id} deleted"}
