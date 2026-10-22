"""
Calendar Events API Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.calendar import CalendarEvent
from app.schemas import CalendarEventCreate, CalendarEventResponse

router = APIRouter(prefix="/api/calendar", tags=["Calendar"])


@router.get("/events", response_model=List[CalendarEventResponse])
def list_calendar_events(
    start: Optional[str] = None,
    end: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List calendar events with optional date range filter."""
    query = db.query(CalendarEvent)
    if start:
        query = query.filter(CalendarEvent.start_time >= start)
    if end:
        query = query.filter(CalendarEvent.end_time <= end)
    return query.order_by(CalendarEvent.start_time).all()


@router.post("/events", response_model=CalendarEventResponse)
def create_calendar_event(event: CalendarEventCreate, db: Session = Depends(get_db)):
    """Create a new calendar event."""
    db_event = CalendarEvent(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.delete("/events/{event_id}")
def delete_calendar_event(event_id: int, db: Session = Depends(get_db)):
    """Delete a calendar event."""
    db_event = db.query(CalendarEvent).filter(CalendarEvent.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted"}
