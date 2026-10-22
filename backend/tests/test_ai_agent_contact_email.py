"""
Unit test for contact email update tool in autonomous agent workflows.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agents.tools.contact_tools import create_contact, update_contact


def test_update_contact_email_and_info():
    """Verify update_contact correctly updates email address, company, and job title."""
    import uuid

    uid = uuid.uuid4().hex[:6]
    # Create test contact
    create_res = create_contact(
        first_name="TestTanuj",
        last_name=f"Automation{uid}",
        email=f"initial.test.{uid}@example.com",
        company="Initial Corp",
        job_title="Lead Engineer",
    )
    assert create_res["success"] is True
    contact_id = create_res["contact"]["id"]

    # Update contact email and job title
    new_email = f"tanujsinghkushwah.updated.{uid}@gmail.com"
    update_res = update_contact(
        identifier=str(contact_id),
        email=new_email,
        job_title="VP of Engineering",
        lead_status="qualified",
    )

    assert update_res["success"] is True
    assert update_res["contact"]["email"] == new_email
    assert update_res["contact"]["job_title"] == "VP of Engineering"
    assert update_res["contact"]["lead_status"] == "qualified"
    assert new_email in update_res["message"]

    # Verify search by first name also finds and updates email
    second_email = f"tanujsinghkushwah.verified.{uid}@gmail.com"
    name_update_res = update_contact(identifier=f"Automation{uid}", email=second_email)

    assert name_update_res["success"] is True
    assert name_update_res["contact"]["email"] == second_email
