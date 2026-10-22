"""
Unit tests for centralized Email Service (SMTP dispatch & CRM Activity logging).
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.services.email_service import send_email_message
from app.database import SessionLocal
from app.models.activity import Activity
from app.models.enums import ActivityType


def test_email_service_logs_activity_when_unconfigured():
    """Verify that send_email_message logs an Activity in CRM when SMTP is unconfigured."""
    res = send_email_message(
        to_email="prospect@acmecorp.com",
        subject="Accelerating RevOps with Autonomous AI",
        body="Hi Alex, here is how NeuronForce helps your team.",
        to_name="Alex Prospect"
    )
    assert res["success"] is True
    assert res["sent_live"] is False
    assert "Email drafted & logged" in res["delivery_status"]
    assert res["activity_id"] is not None

    # Verify Activity recorded in SQLite
    db = SessionLocal()
    try:
        activity = db.query(Activity).filter(Activity.id == res["activity_id"]).first()
        assert activity is not None
        assert activity.type == ActivityType.EMAIL
        assert "Accelerating RevOps" in activity.subject
        assert "prospect@acmecorp.com" in activity.description
    finally:
        db.close()


def test_email_service_smtp_live_dispatch_mocked(monkeypatch):
    """Verify SMTP live delivery when SMTP credentials are configured."""
    monkeypatch.setenv("SMTP_HOST", "smtp.test-provider.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SMTP_USER", "test-user@neuronforce.ai")
    monkeypatch.setenv("SMTP_PASSWORD", "test-password")

    with patch("smtplib.SMTP") as mock_smtp_class:
        mock_instance = MagicMock()
        mock_smtp_class.return_value.__enter__.return_value = mock_instance

        res = send_email_message(
            to_email="tanujsinghkushwah@gmail.com",
            subject="Personalized Outreach: NeuronForce",
            body="Hi Tanuj, thanks for exploring NeuronForce.",
            to_name="Tanuj"
        )

        assert res["success"] is True
        assert res["sent_live"] is True
        assert "Delivered live to tanujsinghkushwah@gmail.com" in res["delivery_status"]
        assert mock_instance.login.called
        assert mock_instance.send_message.called


def test_email_service_resend_live_dispatch_mocked(monkeypatch):
    """Verify Resend API live delivery when RESEND_API_KEY is configured."""
    monkeypatch.setenv("RESEND_API_KEY", "re_test_mock_key_12345")

    with patch("resend.Emails.send") as mock_resend_send:
        mock_resend_send.return_value = {"id": "res_mock_test_id"}

        res = send_email_message(
            to_email="tanujsinghkushwah@gmail.com",
            subject="Hyper-personalized Outreach: NeuronForce",
            body="Hi Tanuj, exploring autonomous AI capabilities.",
            to_name="Tanuj Singh Kushwah"
        )

        assert res["success"] is True
        assert res["sent_live"] is True
        assert res["provider"] == "Resend API"
        assert "Delivered live to tanujsinghkushwah@gmail.com via Resend" in res["delivery_status"]
        assert mock_resend_send.called

