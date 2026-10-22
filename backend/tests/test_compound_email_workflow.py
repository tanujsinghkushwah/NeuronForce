"""
End-to-End test for compound AI agent prompt:
Updating contact email and sequentially drafting/sending personalized sales email.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agents.orchestrator import run_agent_orchestrator
from app.database import SessionLocal
from app.models.contact import Contact
from app.models.activity import Activity
from app.models.enums import ActivityType


def test_compound_prompt_contact_email_and_send_personalized_email():
    """
    Test user prompt:
    'Update email for Tanuj to tanujsinghkushwah@gmail.com and then send a personalized email related to our product NeuronForce'
    """
    # Verify contact Tanuj exists or create if needed
    db = SessionLocal()
    contact = db.query(Contact).filter(Contact.first_name.ilike("%Tanuj%")).first()
    if not contact:
        contact = Contact(
            first_name="Tanuj",
            last_name="Singh Kushwah",
            email="tanuj.singhkushwah@example.com",
            company="Acme Corp",
            lead_score=50
        )
        db.add(contact)
        db.commit()
        db.refresh(contact)
    db.close()

    target_new_email = "tanujsinghkushwah@gmail.com"
    prompt = f"Update email for Tanuj to {target_new_email} and then send a personalized email related to our product NeuronForce"

    res = run_agent_orchestrator(prompt=prompt, session_id="test_session")

    # 1. Verify orchestrator executed CRM action
    assert res["tool_result"] is not None, "tool_result should not be None"
    assert res["tool_result"]["success"] is True, "tool_result should succeed"
    assert res["tool_result"]["contact"]["email"] == target_new_email

    # 2. Verify subagent personalized email was drafted & dispatched/logged
    assert res["subagent_result"] is not None, "subagent_result should not be None"
    assert res["subagent_result"]["email_address"] == target_new_email
    assert "subject" in res["subagent_result"]
    assert "body" in res["subagent_result"]
    assert res["subagent_result"]["dispatch_status"] is not None
    assert res["subagent_result"]["dispatch_status"]["activity_id"] is not None

    # 3. Verify SQLite DB Contact record has updated email
    db = SessionLocal()
    try:
        updated_contact = db.query(Contact).filter(Contact.first_name.ilike("%Tanuj%")).first()
        assert updated_contact is not None
        assert updated_contact.email == target_new_email

        # 4. Verify Activity log has the email recorded
        activity = db.query(Activity).filter(
            Activity.contact_id == updated_contact.id,
            Activity.type == ActivityType.EMAIL
        ).order_by(Activity.id.desc()).first()
        assert activity is not None
        assert target_new_email in activity.description
    finally:
        db.close()

    # 5. Verify synthesized reply contains both update and email body
    assert target_new_email in res["reply"]
    assert res["subagent_result"]["subject"] in res["reply"]
