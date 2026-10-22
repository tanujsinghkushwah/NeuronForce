"""
NeuronForce Centralized Email Service
Handles outbound email dispatch via free Resend API (single API key)
with fallback to Gmail/SMTP or demo CRM Activity logging.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.database import SessionLocal
from app.models.activity import Activity
from app.models.enums import ActivityType


def send_email_message(
    to_email: str,
    subject: str,
    body: str,
    to_name: Optional[str] = None,
    contact_id: Optional[int] = None,
    html_body: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send an email via Resend (single RESEND_API_KEY) or Gmail/SMTP.
    Always records the email as an Activity in the CRM database.
    """
    # Dynamically load from .env if not already present in environment
    if "RESEND_API_KEY" not in os.environ:
        dotenv_path = BACKEND_DIR / ".env"
        if dotenv_path.exists():
            from dotenv import load_dotenv

            load_dotenv(dotenv_path)

    resend_api_key = os.getenv("RESEND_API_KEY", "").strip()

    gmail_user = os.getenv("GMAIL_USER", "").strip()
    gmail_app_password = os.getenv("GMAIL_APP_PASSWORD", "").strip()
    smtp_host = os.getenv("SMTP_HOST", "").strip()
    smtp_user = os.getenv("SMTP_USER", "").strip() or gmail_user
    smtp_password = os.getenv("SMTP_PASSWORD", "").strip() or gmail_app_password

    sent_successfully = False
    delivery_status_msg = ""
    error_detail = None
    provider_used = "CRM Activity Log"

    # Default styled HTML email template
    html_content = (
        html_body
        or f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; background-color: #f8fafc; margin: 0; padding: 24px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }}
        .header {{ background: linear-gradient(135deg, #4f46e5, #06b6d4); padding: 24px; color: white; }}
        .header h1 {{ margin: 0; font-size: 20px; font-weight: 700; }}
        .content {{ padding: 28px; white-space: pre-wrap; font-size: 14px; line-height: 1.7; color: #334155; }}
        .footer {{ background: #f1f5f9; padding: 16px 28px; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>NeuronForce Autonomous Sales</h1>
        </div>
        <div class="content">{body}</div>
        <div class="footer">
          Sent autonomously by NeuronForce AI Sales Studio for {to_name or to_email}.
        </div>
      </div>
    </body>
    </html>
    """
    )

    # 1. Primary Free Method: Resend API (single RESEND_API_KEY)
    if resend_api_key:
        try:
            import resend

            resend.api_key = resend_api_key
            from_sender = (
                os.getenv("SMTP_FROM_EMAIL") or "NeuronForce <onboarding@resend.dev>"
            )
            params: Any = {
                "from": from_sender,
                "to": [to_email],
                "subject": subject,
                "html": html_content,
                "text": body,
            }
            res = resend.Emails.send(params)
            sent_successfully = True
            provider_used = "Resend API"
            delivery_status_msg = (
                f"Delivered live to {to_email} via Resend (ID: {res.get('id', 'sent')})"
            )
        except Exception as exc:
            sent_successfully = False
            error_detail = str(exc)
            delivery_status_msg = f"Resend API attempt failed: {str(exc)}. Recorded in CRM activity trail."

    # 2. Secondary Method: Gmail or SMTP relay (if credentials provided)
    elif smtp_user and smtp_password:
        host = smtp_host or "smtp.gmail.com"
        port = int(os.getenv("SMTP_PORT", "587"))
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            from_name = os.getenv("SMTP_FROM_NAME", "NeuronForce Sales Team")
            from_addr = os.getenv("SMTP_FROM_EMAIL", smtp_user)
            msg["From"] = f"{from_name} <{from_addr}>"
            msg["To"] = f"{to_name} <{to_email}>" if to_name else to_email
            msg["Date"] = datetime.now(timezone.utc).strftime(
                "%a, %d %b %Y %H:%M:%S +0000"
            )
            msg.attach(MIMEText(body, "plain", "utf-8"))
            msg.attach(MIMEText(html_content, "html", "utf-8"))

            with smtplib.SMTP(host, port, timeout=12) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)

            sent_successfully = True
            provider_used = f"SMTP ({host})"
            delivery_status_msg = (
                f"Delivered live to {to_email} via SMTP ({host}:{port})"
            )
        except Exception as exc:
            sent_successfully = False
            error_detail = str(exc)
            delivery_status_msg = f"SMTP relay attempt failed: {str(exc)}. Recorded in CRM activity trail."

    # 3. Demo Fallback: Log email activity in CRM
    else:
        sent_successfully = False
        provider_used = "CRM Activity Log"
        delivery_status_msg = f"Email drafted & logged to CRM activities for {to_email}. (To dispatch live to your inbox, set RESEND_API_KEY in backend/.env - free at resend.com)"

    # Record Activity in CRM Database
    db = SessionLocal()
    activity_id = None
    try:
        activity = Activity(
            type=ActivityType.EMAIL,
            subject=subject[:300],
            description=f"To: {to_email}\nProvider: {provider_used}\nStatus: {'SENT' if sent_successfully else 'LOGGED'}\n\n{body}",
            contact_id=contact_id,
            outcome=delivery_status_msg[:200],
            completed_at=datetime.now(timezone.utc),
            scheduled_at=datetime.now(timezone.utc),
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)
        activity_id = activity.id
    except Exception:
        db.rollback()
    finally:
        db.close()

    return {
        "success": True,
        "sent_live": sent_successfully,
        "recipient": to_email,
        "subject": subject,
        "activity_id": activity_id,
        "delivery_status": delivery_status_msg,
        "provider": provider_used,
        "error": error_detail,
        "configured": bool(resend_api_key or (smtp_user and smtp_password)),
    }
