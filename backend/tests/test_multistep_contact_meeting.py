"""
End-to-End test for multi-step AI agent prompt:
1. Creating a new contact Tanuj with email tanujsinghkushwah@gmail.com
2. Sequentially scheduling a meeting for Tanuj and Sarah for tomorrow 12 PM-1 PM
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agents.orchestrator import run_agent_orchestrator
from app.database import SessionLocal
from app.models.contact import Contact
from app.models.calendar import CalendarEvent


def test_multistep_contact_and_calendar_meeting():
    """
    Test user's exact multi-step prompt:
    'Create a new contact Tanuj with email tanujsinghkushwah@gmail.com
     Then schedule a meeting for Tanuj and Sarah for tomorrow 12 PM-1 PM'
    """
    db = SessionLocal()
    # Ensure Sarah Chen exists
    sarah = db.query(Contact).filter(Contact.first_name.ilike("%Sarah%")).first()
    if not sarah:
        sarah = Contact(
            first_name="Sarah",
            last_name="Chen",
            email="sarah.chen@techcorp.io",
            company="TechCorp Solutions",
            title="VP of Engineering",
            lead_score=92,
        )
        db.add(sarah)
        db.commit()
        db.refresh(sarah)

    # Clean up any existing Tanuj test contact & test events to ensure fresh validation
    existing_tanuj = (
        db.query(Contact).filter(Contact.email == "tanujsinghkushwah@gmail.com").all()
    )
    for c in existing_tanuj:
        db.query(CalendarEvent).filter(CalendarEvent.contact_id == c.id).delete()
        db.delete(c)
    db.commit()
    db.close()

    prompt = (
        "Create a new contact Tanuj with email tanujsinghkushwah@gmail.com\n"
        "Then schedule a meeting for Tanuj and Sarah for tomorrow 12 PM-1 PM"
    )

    res = run_agent_orchestrator(
        prompt=prompt, session_id="test_multistep_contact_meeting"
    )

    # 1. Verify orchestrator executed both CRM actions in sequence
    assert "tool_results" in res, "tool_results key missing from orchestrator response"
    assert (
        len(res["tool_results"]) == 2
    ), f"Expected 2 tool_results, got: {len(res['tool_results'])}"

    contact_action = res["tool_results"][0]
    assert (
        contact_action["success"] is True
    ), f"Contact creation failed: {contact_action}"
    assert contact_action["contact"]["email"] == "tanujsinghkushwah@gmail.com"
    assert "Tanuj" in contact_action["contact"]["name"]

    meeting_action = res["tool_results"][1]
    assert (
        meeting_action["success"] is True
    ), f"Meeting scheduling failed: {meeting_action}"
    assert meeting_action["action"] == "schedule_meeting"
    assert meeting_action["event"]["duration_minutes"] == 60

    # 2. Verify graph steps traversed both actions
    node_names = [s["node"] for s in res["graph_steps"]]
    assert (
        "action_create_contact" in node_names
    ), f"action_create_contact missing from graph steps: {node_names}"
    assert (
        "action_schedule_meeting" in node_names
    ), f"action_schedule_meeting missing from graph steps: {node_names}"

    # 3. Verify SQLite DB state
    db = SessionLocal()
    try:
        created_contact = (
            db.query(Contact)
            .filter(Contact.email == "tanujsinghkushwah@gmail.com")
            .first()
        )
        assert created_contact is not None, "Tanuj was not persisted in database"

        # Check calendar event
        event_id = meeting_action["event"]["id"]
        event = db.query(CalendarEvent).filter(CalendarEvent.id == event_id).first()
        assert event is not None, "CalendarEvent was not persisted in database"
        assert event.contact_id == created_contact.id

        # Check attendees resolved both contacts
        attendees = event.attendees or []
        assert (
            "tanujsinghkushwah@gmail.com" in attendees
        ), f"Tanuj's email missing from attendees: {attendees}"
        assert (
            "sarah.chen@techcorp.io" in attendees
        ), f"Sarah's email missing from attendees: {attendees}"

        # Check timing: tomorrow 12:00 to 13:00
        now = datetime.now()
        expected_tomorrow_date = (now + timedelta(days=1)).date()
        assert (
            event.start_time.date() == expected_tomorrow_date
        ), f"Expected {expected_tomorrow_date}, got {event.start_time.date()}"
        assert event.start_time.hour == 12
        assert event.start_time.minute == 0
        assert event.end_time.hour == 13
        assert event.end_time.minute == 0
    finally:
        db.close()
