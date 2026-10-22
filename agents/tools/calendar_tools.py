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
    default_duration: Optional[int] = 45,
) -> tuple[datetime, datetime, int]:
    """
    Intelligently parses ISO strings, natural language, date/time ranges, and relative expressions.
    Returns: (start_datetime, end_datetime, duration_minutes)
    """
    now = datetime.now()
    ref_date = now.replace(minute=0, second=0, microsecond=0)
    dur = default_duration or 45

    if not start_str or not str(start_str).strip():
        st = (ref_date + timedelta(days=1)).replace(
            hour=14, minute=0, second=0, microsecond=0
        )
        return st, st + timedelta(minutes=dur), dur

    s = str(start_str).strip()

    # Pre-process relative date expressions before parsing
    def replace_relative_dates(text: str) -> str:
        res = text
        res = re.sub(
            r"\btomorrow\b",
            (now + timedelta(days=1)).strftime("%Y-%m-%d"),
            res,
            flags=re.IGNORECASE,
        )
        res = re.sub(
            r"\btoday\b",
            now.strftime("%Y-%m-%d"),
            res,
            flags=re.IGNORECASE,
        )
        res = re.sub(
            r"\byesterday\b",
            (now - timedelta(days=1)).strftime("%Y-%m-%d"),
            res,
            flags=re.IGNORECASE,
        )
        days_ahead = (0 - now.weekday() + 7) % 7 or 7
        res = re.sub(
            r"\bnext monday\b",
            (now + timedelta(days=days_ahead)).strftime("%Y-%m-%d"),
            res,
            flags=re.IGNORECASE,
        )
        return res

    s = replace_relative_dates(s)
    if end_str:
        end_str = replace_relative_dates(str(end_str))

    # 1. If explicit end_str is provided
    if end_str and str(end_str).strip():
        try:
            st = date_parser.parse(s, default=ref_date)
            en = date_parser.parse(str(end_str).strip(), default=st)
            computed_dur = max(15, int((en - st).total_seconds() / 60))
            return st, en, computed_dur
        except Exception:
            pass

    # 2. Check for time range pattern in start_str:
    # Matches patterns like "2026-10-24 12 PM-1 PM" or "12 PM-1 PM 2026-10-24" or "12:00 PM - 1:00 PM"
    m_prefix = re.search(
        r"(.*?)\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)\s*(?:-|–|to)\s*(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)(.*)",
        s,
        re.IGNORECASE,
    )
    m_range = re.search(
        r"(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)\s*(?:-|–|to)\s*(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)(.*)",
        s,
        re.IGNORECASE,
    )

    start_t, end_t, date_part = None, None, None
    if m_prefix and m_prefix.group(1).strip():
        date_part = m_prefix.group(1).strip() + " " + (m_prefix.group(4) or "").strip()
        start_t = m_prefix.group(2).strip()
        end_t = m_prefix.group(3).strip()
    elif m_range:
        start_t = m_range.group(1).strip()
        end_t = m_range.group(2).strip()
        date_part = (m_range.group(3) or "").strip()

    if start_t and end_t:
        # Propagate AM/PM if only end_t specifies it (e.g. "12 - 1 PM" -> "12 PM - 1 PM")
        if any(x in end_t.lower() for x in ["am", "pm"]) and not any(
            x in start_t.lower() for x in ["am", "pm"]
        ):
            ampm = "PM" if "pm" in end_t.lower() else "AM"
            start_t = f"{start_t} {ampm}"
        try:
            target_date_str = (date_part or "").strip() or ref_date.strftime("%Y-%m-%d")
            base_default = ref_date.replace(hour=12, minute=0, second=0)
            st = date_parser.parse(f"{target_date_str} {start_t}", default=base_default)
            en = date_parser.parse(f"{target_date_str} {end_t}", default=st)
            if en <= st:
                en = en + timedelta(hours=12)  # Handles cases crossing 12 PM
            computed_dur = max(15, int((en - st).total_seconds() / 60))
            return st, en, computed_dur
        except Exception:
            pass

    # 3. Standard dateutil parsing
    try:
        base_default = ref_date.replace(hour=12, minute=0, second=0)
        st = date_parser.parse(s, default=base_default)
        en = st + timedelta(minutes=dur)
        return st, en, dur
    except Exception:
        st = (now + timedelta(days=1)).replace(
            hour=14, minute=0, second=0, microsecond=0
        )
        return st, st + timedelta(minutes=45), 45


def schedule_meeting(
    title: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    duration_minutes: Optional[int] = None,
    attendees: Optional[List[str]] = None,
    location: str = "Google Meet / Zoom",
    description: str = "",
    event_type: str = "client_meeting",
    contact_id: Optional[int] = None,
    deal_id: Optional[int] = None,
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
            default_duration=duration_minutes or 45,
        )

        event = CalendarEvent(
            title=title,
            description=description
            or f"Autonomous Sales Agent scheduled meeting: {title}",
            start_time=dt_start,
            end_time=dt_end,
            location=location,
            event_type=event_type,
            attendees=attendees or ["team@neuronforce.ai"],
            color="#6366f1",
            is_all_day=False,
            reminder_minutes=15,
            contact_id=contact_id,
            deal_id=deal_id,
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
            "message": f"Successfully scheduled '{event.title}' on {formatted_time} ({actual_duration} mins).",
        }
    except Exception as exc:
        db.rollback()
        return {
            "success": False,
            "action": "schedule_meeting",
            "error": str(exc),
            "message": f"Failed to schedule meeting: {str(exc)}",
        }
    finally:
        db.close()


def update_meeting(
    event_id: int,
    title: Optional[str] = None,
    start_time: Optional[str] = None,
    location: Optional[str] = None,
) -> Dict[str, Any]:
    """Update an existing calendar event."""
    db = SessionLocal()
    try:
        event = db.query(CalendarEvent).filter(CalendarEvent.id == event_id).first()
        if not event:
            return {
                "success": False,
                "message": f"Calendar event #{event_id} not found.",
            }

        if title:
            setattr(event, "title", title)
        if location:
            setattr(event, "location", location)
        if start_time:
            try:
                setattr(
                    event,
                    "start_time",
                    datetime.fromisoformat(start_time.replace("Z", "+00:00")),
                )
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
            "message": f"Updated meeting '{event.title}'.",
        }
    except Exception as exc:
        db.rollback()
        return {
            "success": False,
            "error": str(exc),
            "message": f"Failed to update meeting: {str(exc)}",
        }
    finally:
        db.close()
