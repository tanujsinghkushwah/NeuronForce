"""
Activities and Tasks API Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from app.database import get_db
from app.models.activity import Activity, Task
from app.schemas import ActivityCreate, ActivityResponse, TaskCreate, TaskResponse

router = APIRouter(prefix="/api", tags=["Activities & Tasks"])


# --- Activities ---


@router.get("/activities", response_model=List[ActivityResponse])
def list_activities(
    skip: int = 0,
    limit: int = 50,
    contact_id: Optional[int] = None,
    deal_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """List activities with optional filtering."""
    query = db.query(Activity)
    if contact_id:
        query = query.filter(Activity.contact_id == contact_id)
    if deal_id:
        query = query.filter(Activity.deal_id == deal_id)
    return query.order_by(desc(Activity.created_at)).offset(skip).limit(limit).all()


@router.post("/activities", response_model=ActivityResponse)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    """Create a new activity."""
    db_activity = Activity(**activity.model_dump())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


# --- Tasks ---


@router.get("/tasks", response_model=List[TaskResponse])
def list_tasks(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List tasks with optional filtering."""
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    return query.order_by(desc(Task.created_at)).offset(skip).limit(limit).all()


@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
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
