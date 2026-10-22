"""
Calendar Tools for Autonomous Agents
Schedules, reschedules, and manages meetings in the CRM database.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional, List

CURRENT_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = CURRENT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.database import SessionLocal
from app.models.calendar import CalendarEvent


import re
from dateutil import parser as date_parser


def parse_meeting_datetime(
    start_str: Optional[str],
    end_str: Optional[str] = None,
    default_duration: Optional[int] = 45
) -> tuple[datetime, datetime, int]:
    """
    Intelligently parses ISO strings, natural language, date/time ranges, and relative expressions.
    Returns: (start_datetime, end_datetime, duration_minutes)
    """
    # System CRM anchor reference: Oct 22, 2026
    ref_date = datetime(2026, 10, 22, 12, 0, 0)
    dur = default_duration or 45

    if not start_str or not str(start_str).strip():
        st = (ref_date + timedelta(days=1)).replace(hour=14, minute=0, second=0, microsecond=0)
        return st, st + timedelta(minutes=dur), dur

    s = str(start_str).strip()

    # 1. If explicit end_str is provided
    if end_str and str(end_str).strip():
        try:
            st = date_parser.parse(s, default=ref_date)
            en = date_parser.parse(str(end_str).strip(), default=st)
            computed_dur = max(15, int((en - st).total_seconds() / 60))
            return st, en, computed_dur
        except Exception:
            pass

    # 2. Check for time range in start_str: "9 PM-10 PM 24 October" or "24 October 9 PM-10 PM"
    m1 = re.search(r"(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)\s*(?:-|to)\s*(\d{1,2}(?::\d{2})?\s*(?:am|pm))\s+(.*)", s, re.IGNORECASE)
    m2 = re.search(r"(.*?)\s+(?:at\s+)?(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)\s*(?:-|to)\s*(\d{1,2}(?::\d{2})?\s*(?:am|pm))", s, re.IGNORECASE)

    start_t, end_t, date_part = None, None, None
    if m1:
        start_t, end_t, date_part = m1.groups()
    elif m2:
        date_part, start_t, end_t = m2.groups()

    if start_t and end_t and date_part:
        if ("am" in end_t.lower() or "pm" in end_t.lower()) and not ("am" in start_t.lower() or "pm" in start_t.lower()):
            ampm = "PM" if "pm" in end_t.lower() else "AM"
            start_t = f"{start_t} {ampm}"
        try:
            st = date_parser.parse(f"{date_part} {start_t}", default=ref_date)
            en = date_parser.parse(f"{date_part} {end_t}", default=st)
            computed_dur = max(15, int((en - st).total_seconds() / 60))
            return st, en, computed_dur
        except Exception:
            pass

    # 3. Relative date replacements
    lower = s.lower()
    if "tomorrow" in lower:
        target_date = (ref_date + timedelta(days=1)).date()
        s = re.sub(r"\btomorrow\b", target_date.strftime("%Y-%m-%d"), s, flags=re.IGNORECASE)
    elif "today" in lower:
        s = re.sub(r"\btoday\b", ref_date.strftime("%Y-%m-%d"), s, flags=re.IGNORECASE)
    elif "next monday" in lower:
        days_ahead = (0 - ref_date.weekday() + 7) % 7 or 7
        target_date = (ref_date + timedelta(days=days_ahead)).date()
        s = re.sub(r"\bnext monday\b", target_date.strftime("%Y-%m-%d"), s, flags=re.IGNORECASE)

    # 4. Standard dateutil parsing
    try:
        st = date_parser.parse(s, default=ref_date)
        en = st + timedelta(minutes=dur)
        return st, en, dur
    except Exception:
        st = (ref_date + timedelta(days=1)).replace(hour=14, minute=0, second=0, microsecond=0)
        return st, st + timedelta(minutes=45), 45


def schedule_meeting(
    title: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    duration_minutes: Optional[int] = None,
    attendees: Optional[List[str]] = None,
    location: str = "Google Meet / Zoom",
    description: str = "",
    event_type: str = "client_meeting"
) -> Dict[str, Any]:
    """
    Schedule a meeting in the CRM calendar.
    Automatically parses natural language, relative dates, and explicit time ranges.
    """
    db = SessionLocal()
    try:
        dt_start, dt_end, actual_duration = parse_meeting_datetime(
            start_str=start_time,
            end_str=end_time,
            default_duration=duration_minutes or 45
        )

        event = CalendarEvent(
            title=title,
            description=description or f"Autonomous Sales Agent scheduled meeting: {title}",
            start_time=dt_start,
            end_time=dt_end,
            location=location,
            event_type=event_type,
            attendees=attendees or ["team@neuronforce.ai"],
            color="#6366f1",
            is_all_day=False,
            reminder_minutes=15
        )
        db.add(event)
        db.commit()
        db.refresh(event)

        formatted_time = f"{event.start_time.strftime('%A, %b %d, %Y from %I:%M %p')} to {event.end_time.strftime('%I:%M %p')}"
        return {
            "success": True,
            "action": "schedule_meeting",
            "event": {
                "id": event.id,
                "title": event.title,
                "start_time": event.start_time.isoformat(),
                "end_time": event.end_time.isoformat(),
                "duration_minutes": actual_duration,
                "location": event.location,
                "attendees": event.attendees,
            },
            "message": f"Successfully scheduled '{event.title}' on {formatted_time} ({actual_duration} mins)."
        }
    except Exception as exc:
        db.rollback()
        return {
            "success": False,
            "action": "schedule_meeting",
            "error": str(exc),
            "message": f"Failed to schedule meeting: {str(exc)}"
        }
    finally:
        db.close()



def update_meeting(
    event_id: int,
    title: Optional[str] = None,
    start_time: Optional[str] = None,
    location: Optional[str] = None
) -> Dict[str, Any]:
    """Update an existing calendar event."""
    db = SessionLocal()
    try:
        event = db.query(CalendarEvent).filter(CalendarEvent.id == event_id).first()
        if not event:
            return {"success": False, "message": f"Calendar event #{event_id} not found."}

        if title:
            event.title = title
        if location:
            event.location = location
        if start_time:
            try:
                event.start_time = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            except Exception:
                pass

        db.commit()
        db.refresh(event)
        return {
            "success": True,
            "action": "update_meeting",
            "event": {
                "id": event.id,
                "title": event.title,
                "start_time": event.start_time.isoformat(),
                "location": event.location,
            },
            "message": f"Updated meeting '{event.title}'."
        }
    except Exception as exc:
        db.rollback()
        return {"success": False, "error": str(exc), "message": f"Failed to update meeting: {str(exc)}"}
    finally:
        db.close()
