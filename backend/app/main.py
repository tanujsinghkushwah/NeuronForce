"""
NeuronForce - AI-Powered CRM Platform Backend
FastAPI application with comprehensive REST API endpoints.
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timezone, timedelta
import random
import time

from .database import engine, get_db, Base
from .models import (
    Contact, Deal, Activity, Task, AIAgentTask, AnalyticsSnapshot,
    CalendarEvent, DealStage, AgentTaskStatus, AgentTaskType
)
from .schemas import (
    ContactCreate, ContactUpdate, ContactResponse,
    DealCreate, DealUpdate, DealResponse,
    ActivityCreate, ActivityResponse,
    TaskCreate, TaskResponse,
    AIAgentTaskCreate, AIAgentTaskResponse,
    CalendarEventCreate, CalendarEventResponse,
    DashboardStats, PipelineView
)
from .seed_data import seed_database

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NeuronForce API",
    description="AI-Powered CRM Platform - Alternative to Salesforce",
    version="1.0.0",
)

# CORS - allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """Initialize database with seed data on startup."""
    db = next(get_db())
    try:
        seed_database(db)
    finally:
        db.close()


# ===================== DASHBOARD =====================

@app.get("/api/dashboard", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get comprehensive dashboard statistics."""
    total_contacts = db.query(Contact).count()
    total_deals = db.query(Deal).count()

    # Revenue from closed-won deals
    total_revenue = db.query(func.coalesce(func.sum(Deal.value), 0)).filter(
        Deal.stage == DealStage.CLOSED_WON
    ).scalar()

    # Pipeline value (active deals)
    pipeline_value = db.query(func.coalesce(func.sum(Deal.value), 0)).filter(
        Deal.stage.notin_([DealStage.CLOSED_WON, DealStage.CLOSED_LOST])
    ).scalar()

    deals_won = db.query(Deal).filter(Deal.stage == DealStage.CLOSED_WON).count()
    deals_lost = db.query(Deal).filter(Deal.stage == DealStage.CLOSED_LOST).count()
    active_deals = db.query(Deal).filter(
        Deal.stage.notin_([DealStage.CLOSED_WON, DealStage.CLOSED_LOST])
    ).count()

    total_closed = deals_won + deals_lost
    conversion_rate = (deals_won / total_closed * 100) if total_closed > 0 else 0
    avg_deal_size = (total_revenue / deals_won) if deals_won > 0 else 0

    # AI task stats for today
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0)
    ai_tasks_today = db.query(AIAgentTask).filter(AIAgentTask.created_at >= today_start).count()
    ai_cost_today = db.query(func.coalesce(func.sum(AIAgentTask.actual_cost), 0)).filter(
        AIAgentTask.created_at >= today_start
    ).scalar()

    # Revenue trend (last 30 days from analytics snapshots)
    snapshots = db.query(AnalyticsSnapshot).order_by(AnalyticsSnapshot.date).limit(30).all()
    revenue_trend = [{"date": s.date.isoformat(), "revenue": s.total_revenue, "pipeline": s.pipeline_value} for s in snapshots]

    # Pipeline by stage
    pipeline_by_stage = []
    for stage in DealStage:
        stage_deals = db.query(Deal).filter(Deal.stage == stage).all()
        stage_value = sum(d.value or 0 for d in stage_deals)
        pipeline_by_stage.append({
            "stage": stage.value,
            "count": len(stage_deals),
            "value": stage_value,
        })

    # Top deals
    top_deals = db.query(Deal).filter(
        Deal.stage.notin_([DealStage.CLOSED_WON, DealStage.CLOSED_LOST])
    ).order_by(desc(Deal.value)).limit(5).all()
    top_deals_data = [{"id": d.id, "title": d.title, "value": d.value, "stage": d.stage.value,
                       "company": d.company, "probability": d.probability} for d in top_deals]

    # Recent activities
    recent = db.query(Activity).order_by(desc(Activity.created_at)).limit(10).all()
    recent_data = [{"id": a.id, "type": a.type.value, "subject": a.subject,
                    "created_at": a.created_at.isoformat()} for a in recent]

    # Lead sources
    sources = db.query(Contact.source, func.count(Contact.id)).group_by(Contact.source).all()
    lead_sources = [{"source": s[0] or "Unknown", "count": s[1]} for s in sources]

    return DashboardStats(
        total_contacts=total_contacts,
        total_deals=total_deals,
        total_revenue=total_revenue,
        pipeline_value=pipeline_value,
        conversion_rate=round(conversion_rate, 1),
        avg_deal_size=round(avg_deal_size, 2),
        deals_won=deals_won,
        deals_lost=deals_lost,
        active_deals=active_deals,
        ai_tasks_today=ai_tasks_today,
        ai_cost_today=round(ai_cost_today, 4),
        revenue_trend=revenue_trend,
        pipeline_by_stage=pipeline_by_stage,
        top_deals=top_deals_data,
        recent_activities=recent_data,
        lead_sources=lead_sources,
    )


# ===================== CONTACTS =====================

@app.get("/api/contacts", response_model=List[ContactResponse])
def list_contacts(
    skip: int = 0,
    limit: int = 50,
    search: Optional[str] = None,
    status: Optional[str] = None,
    sort_by: Optional[str] = "created_at",
    db: Session = Depends(get_db)
):
    """List contacts with optional filtering and search."""
    query = db.query(Contact)
    if search:
        query = query.filter(
            (Contact.first_name.ilike(f"%{search}%")) |
            (Contact.last_name.ilike(f"%{search}%")) |
            (Contact.email.ilike(f"%{search}%")) |
            (Contact.company.ilike(f"%{search}%"))
        )
    if status:
        query = query.filter(Contact.lead_status == status)
    query = query.order_by(desc(Contact.created_at))
    return query.offset(skip).limit(limit).all()


@app.get("/api/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """Get a specific contact by ID."""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@app.post("/api/contacts", response_model=ContactResponse)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    """Create a new contact."""
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@app.put("/api/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    """Update a contact."""
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    update_data = contact.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@app.delete("/api/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """Delete a contact."""
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact deleted"}


# ===================== DEALS =====================

@app.get("/api/deals", response_model=List[DealResponse])
def list_deals(
    skip: int = 0,
    limit: int = 50,
    stage: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List deals with optional filtering."""
    query = db.query(Deal)
    if stage:
        query = query.filter(Deal.stage == stage)
    if search:
        query = query.filter(
            (Deal.title.ilike(f"%{search}%")) |
            (Deal.company.ilike(f"%{search}%"))
        )
    query = query.order_by(desc(Deal.created_at))
    return query.offset(skip).limit(limit).all()


@app.get("/api/deals/pipeline")
def get_pipeline(db: Session = Depends(get_db)):
    """Get deals organized by pipeline stage."""
    pipeline = {}
    total_value = 0
    weighted_value = 0

    for stage in DealStage:
        deals = db.query(Deal).filter(Deal.stage == stage).order_by(desc(Deal.value)).all()
        pipeline[stage.value] = []
        for d in deals:
            deal_data = {
                "id": d.id, "title": d.title, "value": d.value,
                "company": d.company, "probability": d.probability,
                "owner": d.owner, "priority": d.priority.value if d.priority else "medium",
                "expected_close_date": d.expected_close_date.isoformat() if d.expected_close_date else None,
                "ai_win_probability": d.ai_win_probability,
                "tags": d.tags or [],
                "contacts": [{"id": c.id, "name": f"{c.first_name} {c.last_name}",
                             "avatar_url": c.avatar_url} for c in d.contacts],
            }
            pipeline[stage.value].append(deal_data)
            if stage not in [DealStage.CLOSED_WON, DealStage.CLOSED_LOST]:
                total_value += d.value or 0
                weighted_value += (d.value or 0) * (d.probability or 0) / 100

    return {"stages": pipeline, "total_value": total_value, "weighted_value": round(weighted_value, 2)}


@app.get("/api/deals/{deal_id}", response_model=DealResponse)
def get_deal(deal_id: int, db: Session = Depends(get_db)):
    """Get a specific deal by ID."""
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@app.post("/api/deals", response_model=DealResponse)
def create_deal(deal: DealCreate, db: Session = Depends(get_db)):
    """Create a new deal."""
    deal_data = deal.model_dump(exclude={"contact_ids"})
    db_deal = Deal(**deal_data)
    if deal.contact_ids:
        contacts = db.query(Contact).filter(Contact.id.in_(deal.contact_ids)).all()
        db_deal.contacts = contacts
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    return db_deal


@app.put("/api/deals/{deal_id}", response_model=DealResponse)
def update_deal(deal_id: int, deal: DealUpdate, db: Session = Depends(get_db)):
    """Update a deal."""
    db_deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not db_deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    update_data = deal.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_deal, key, value)
    db.commit()
    db.refresh(db_deal)
    return db_deal


@app.delete("/api/deals/{deal_id}")
def delete_deal(deal_id: int, db: Session = Depends(get_db)):
    """Delete a deal."""
    db_deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not db_deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    db.delete(db_deal)
    db.commit()
    return {"message": "Deal deleted"}


# ===================== ACTIVITIES =====================

@app.get("/api/activities", response_model=List[ActivityResponse])
def list_activities(
    skip: int = 0,
    limit: int = 50,
    contact_id: Optional[int] = None,
    deal_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """List activities with optional filtering."""
    query = db.query(Activity)
    if contact_id:
        query = query.filter(Activity.contact_id == contact_id)
    if deal_id:
        query = query.filter(Activity.deal_id == deal_id)
    return query.order_by(desc(Activity.created_at)).offset(skip).limit(limit).all()


@app.post("/api/activities", response_model=ActivityResponse)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    """Create a new activity."""
    db_activity = Activity(**activity.model_dump())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


# ===================== TASKS =====================

@app.get("/api/tasks", response_model=List[TaskResponse])
def list_tasks(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List tasks with optional filtering."""
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    return query.order_by(desc(Task.created_at)).offset(skip).limit(limit).all()


@app.post("/api/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    """Update a task."""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


# ===================== AI AGENTS =====================

@app.get("/api/ai-agents/tasks", response_model=List[AIAgentTaskResponse])
def list_ai_tasks(
    skip: int = 0,
    limit: int = 20,
    task_type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List AI agent tasks."""
    query = db.query(AIAgentTask)
    if task_type:
        query = query.filter(AIAgentTask.task_type == task_type)
    if status:
        query = query.filter(AIAgentTask.status == status)
    return query.order_by(desc(AIAgentTask.created_at)).offset(skip).limit(limit).all()


@app.post("/api/ai-agents/tasks", response_model=AIAgentTaskResponse)
def create_ai_task(task: AIAgentTaskCreate, db: Session = Depends(get_db)):
    """Create and execute an AI agent task (simulated for MVP)."""
    start_time = time.time()

    # Simulate AI processing with realistic outputs
    ai_outputs = _simulate_ai_task(task.task_type, task.input_data)

    latency_ms = int((time.time() - start_time) * 1000) + random.randint(200, 2000)

    db_task = AIAgentTask(
        task_type=task.task_type,
        status=AgentTaskStatus.COMPLETED,
        input_data=task.input_data,
        output_data=ai_outputs["output"],
        confidence_score=ai_outputs["confidence"],
        cost_estimate=ai_outputs["cost"] * 1.1,
        actual_cost=ai_outputs["cost"],
        latency_ms=latency_ms,
        triggered_by=task.triggered_by or "user",
        completed_at=datetime.now(timezone.utc),
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/api/ai-agents/stats")
def get_ai_stats(db: Session = Depends(get_db)):
    """Get AI agent performance statistics."""
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

    # Cost breakdown by task type
    cost_by_type = db.query(
        AIAgentTask.task_type,
        func.sum(AIAgentTask.actual_cost),
        func.count(AIAgentTask.id),
        func.avg(AIAgentTask.latency_ms)
    ).group_by(AIAgentTask.task_type).all()

    return {
        "total_tasks": total_tasks,
        "completed": completed,
        "failed": failed,
        "running": running,
        "success_rate": round(completed / total_tasks * 100, 1) if total_tasks > 0 else 0,
        "total_cost": round(total_cost, 4),
        "avg_latency_ms": round(avg_latency, 0),
        "avg_confidence": round(avg_confidence, 2),
        "cost_by_type": [
            {"type": c[0].value if hasattr(c[0], 'value') else c[0], "cost": round(c[1] or 0, 4),
             "count": c[2], "avg_latency": round(c[3] or 0, 0)}
            for c in cost_by_type
        ],
        "cost_efficiency": {
            "cost_per_task": round(total_cost / total_tasks, 4) if total_tasks > 0 else 0,
            "roi_estimate": round(total_cost * 150, 2),  # Simulated ROI multiplier
            "time_saved_hours": round(total_tasks * 0.5, 1),  # Est. 30 min saved per task
        }
    }


def _simulate_ai_task(task_type: str, input_data: dict) -> dict:
    """Simulate AI task execution for MVP demo."""
    simulations = {
        "lead_scoring": {
            "output": {
                "score": random.randint(40, 98),
                "factors": random.sample([
                    "High email engagement rate", "Budget confirmed", "Decision maker identified",
                    "Active website visitor", "Downloaded whitepaper", "Attended webinar",
                    "Multiple touchpoints", "Matches ideal customer profile"
                ], k=3),
                "recommendation": random.choice([
                    "Prioritize for immediate outreach",
                    "Schedule discovery call this week",
                    "Nurture with content sequence",
                    "Assign to senior sales rep"
                ]),
            },
            "confidence": round(random.uniform(0.75, 0.96), 2),
            "cost": round(random.uniform(0.001, 0.005), 4),
        },
        "email_draft": {
            "output": {
                "subject": "Re: Partnership Opportunity - Next Steps",
                "body": "Dear [Contact],\n\nThank you for your time during our recent conversation. I wanted to follow up with some additional details about how our platform can address the challenges you mentioned...\n\nBest regards,\nYour Sales Team",
                "tone_analysis": "Professional, Engaging",
                "alternatives": 3,
            },
            "confidence": round(random.uniform(0.80, 0.92), 2),
            "cost": round(random.uniform(0.005, 0.015), 4),
        },
        "deal_analysis": {
            "output": {
                "risk_level": random.choice(["low", "medium", "high"]),
                "win_probability": round(random.uniform(0.3, 0.9), 2),
                "key_risks": random.sample([
                    "Budget constraints", "Competitor presence", "Long decision cycle",
                    "Missing champion", "Technical requirements gap"
                ], k=2),
                "mitigation_strategies": random.sample([
                    "Offer flexible pricing", "Demonstrate unique value",
                    "Engage executive sponsor", "Provide reference customers",
                    "Arrange technical POC"
                ], k=2),
            },
            "confidence": round(random.uniform(0.70, 0.88), 2),
            "cost": round(random.uniform(0.01, 0.03), 4),
        },
        "churn_prediction": {
            "output": {
                "at_risk_accounts": [
                    {"company": "Sample Corp", "churn_probability": round(random.uniform(0.2, 0.7), 2),
                     "signals": ["Decreased usage", "Support escalation"]},
                ],
                "total_revenue_at_risk": random.randint(50000, 500000),
                "recommended_interventions": ["Executive check-in", "Feature training session"],
            },
            "confidence": round(random.uniform(0.68, 0.85), 2),
            "cost": round(random.uniform(0.02, 0.05), 4),
        },
        "forecast": {
            "output": {
                "predicted_revenue": random.randint(1500000, 4000000),
                "confidence_interval": [random.randint(1200000, 1800000), random.randint(3500000, 4500000)],
                "key_drivers": ["Pipeline momentum", "Seasonal trends", "Market conditions"],
                "risk_adjusted_forecast": random.randint(1400000, 3500000),
            },
            "confidence": round(random.uniform(0.65, 0.82), 2),
            "cost": round(random.uniform(0.03, 0.08), 4),
        },
        "meeting_summary": {
            "output": {
                "summary": "Discussion covered Q4 pipeline status, key deal updates, and action items for the team.",
                "key_points": ["Pipeline at $2.8M", "3 deals in negotiation", "Need more enterprise leads"],
                "action_items": ["Follow up with TechCorp by Friday", "Prepare ROI deck for HealthTech"],
                "sentiment": "Positive, action-oriented",
            },
            "confidence": round(random.uniform(0.82, 0.95), 2),
            "cost": round(random.uniform(0.008, 0.02), 4),
        },
    }

    return simulations.get(task_type, {
        "output": {"message": "Task processed successfully"},
        "confidence": 0.8,
        "cost": 0.01,
    })


# ===================== CALENDAR =====================

@app.get("/api/calendar/events", response_model=List[CalendarEventResponse])
def list_calendar_events(
    start: Optional[str] = None,
    end: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List calendar events with optional date range filter."""
    query = db.query(CalendarEvent)
    if start:
        query = query.filter(CalendarEvent.start_time >= start)
    if end:
        query = query.filter(CalendarEvent.end_time <= end)
    return query.order_by(CalendarEvent.start_time).all()


@app.post("/api/calendar/events", response_model=CalendarEventResponse)
def create_calendar_event(event: CalendarEventCreate, db: Session = Depends(get_db)):
    """Create a new calendar event."""
    db_event = CalendarEvent(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@app.delete("/api/calendar/events/{event_id}")
def delete_calendar_event(event_id: int, db: Session = Depends(get_db)):
    """Delete a calendar event."""
    db_event = db.query(CalendarEvent).filter(CalendarEvent.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted"}


# ===================== ANALYTICS =====================

@app.get("/api/analytics/revenue")
def get_revenue_analytics(days: int = 30, db: Session = Depends(get_db)):
    """Get revenue analytics over time."""
    snapshots = db.query(AnalyticsSnapshot).order_by(
        desc(AnalyticsSnapshot.date)
    ).limit(days).all()
    snapshots.reverse()
    return [{
        "date": s.date.isoformat(),
        "total_revenue": s.total_revenue,
        "pipeline_value": s.pipeline_value,
        "deals_won": s.deals_won,
        "deals_lost": s.deals_lost,
        "conversion_rate": s.conversion_rate,
        "avg_deal_size": s.avg_deal_size,
        "new_contacts": s.new_contacts,
        "ai_tasks_run": s.ai_tasks_run,
        "ai_total_cost": s.ai_total_cost,
    } for s in snapshots]


@app.get("/api/analytics/performance")
def get_performance_metrics(db: Session = Depends(get_db)):
    """Get performance metrics for the team."""
    owners = db.query(Deal.owner, func.count(Deal.id), func.sum(Deal.value)).group_by(Deal.owner).all()

    return {
        "team_performance": [
            {
                "owner": o[0] or "Unassigned",
                "deal_count": o[1],
                "total_value": round(o[2] or 0, 2),
                "avg_value": round((o[2] or 0) / o[1], 2) if o[1] > 0 else 0,
            }
            for o in owners
        ],
        "overall": {
            "total_pipeline": db.query(func.coalesce(func.sum(Deal.value), 0)).filter(
                Deal.stage.notin_([DealStage.CLOSED_WON, DealStage.CLOSED_LOST])
            ).scalar(),
            "total_revenue": db.query(func.coalesce(func.sum(Deal.value), 0)).filter(
                Deal.stage == DealStage.CLOSED_WON
            ).scalar(),
            "avg_sales_cycle": random.randint(25, 45),  # Simulated for MVP
        }
    }


# ===================== SETTINGS =====================

@app.get("/api/settings")
def get_settings():
    """Get application settings."""
    return {
        "company": {
            "name": "NeuronForce",
            "timezone": "America/Los_Angeles",
            "currency": "USD",
            "fiscal_year_start": "January",
        },
        "ai_config": {
            "auto_lead_scoring": True,
            "auto_email_drafts": True,
            "churn_prediction_enabled": True,
            "forecast_model": "ensemble",
            "max_daily_budget": 5.00,
            "confidence_threshold": 0.7,
            "model_provider": "multi-model",
            "cost_optimization": True,
        },
        "notifications": {
            "email_alerts": True,
            "deal_stage_changes": True,
            "ai_task_completion": True,
            "daily_digest": True,
        },
        "pipeline_stages": [
            {"key": "prospecting", "label": "Prospecting", "probability": 10},
            {"key": "qualification", "label": "Qualification", "probability": 25},
            {"key": "proposal", "label": "Proposal", "probability": 50},
            {"key": "negotiation", "label": "Negotiation", "probability": 75},
            {"key": "closed_won", "label": "Closed Won", "probability": 100},
            {"key": "closed_lost", "label": "Closed Lost", "probability": 0},
        ]
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0", "timestamp": datetime.now(timezone.utc).isoformat()}
