"""
NeuronForce Centralized Email Service
Handles outbound email dispatch via standard SMTP (Gmail App Password, SendGrid, AWS SES, or custom relay)
with automatic fallback to CRM Activity logging when live credentials are not yet configured.
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
    Attempt to send an email via SMTP.
    If SMTP credentials are configured in .env, delivers to the recipient's real inbox.
    Always records the email as an Activity in the CRM database.
    """
    smtp_host = os.getenv("SMTP_HOST", "")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    from_email = os.getenv("SMTP_FROM_EMAIL", smtp_user or "sales@neuronforce.ai")
    from_name = os.getenv("SMTP_FROM_NAME", "NeuronForce Sales Team")
    use_tls = os.getenv("SMTP_USE_TLS", "true").lower() in ("true", "1", "yes")

    # If host is omitted but user is gmail, default to smtp.gmail.com
    if not smtp_host and smtp_user and "@gmail.com" in smtp_user:
        smtp_host = "smtp.gmail.com"
        smtp_port = 587
    elif not smtp_host and smtp_user == "apikey":
        smtp_host = "smtp.sendgrid.net"
        smtp_port = 587

    smtp_configured = bool(smtp_host and smtp_user and smtp_password)
    sent_successfully = False
    delivery_status_msg = ""
    error_detail = None

    if smtp_configured:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{from_name} <{from_email}>"
            msg["To"] = f"{to_name} <{to_email}>" if to_name else to_email
            msg["Date"] = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

            # Plain text part
            msg.attach(MIMEText(body, "plain", "utf-8"))

            # HTML part
            html_content = html_body or f"""
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
                  Sent autonomously by NeuronForce Sales Studio for {to_name or to_email}.
                </div>
              </div>
            </body>
            </html>
            """
            msg.attach(MIMEText(html_content, "html", "utf-8"))

            if smtp_port == 465:
                with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=12) as server:
                    server.login(smtp_user, smtp_password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(smtp_host, smtp_port, timeout=12) as server:
                    if use_tls:
                        server.starttls()
                    server.login(smtp_user, smtp_password)
                    server.send_message(msg)

            sent_successfully = True
            delivery_status_msg = f"Delivered live to {to_email} via SMTP ({smtp_host}:{smtp_port})"
        except Exception as exc:
            sent_successfully = False
            error_detail = str(exc)
            delivery_status_msg = f"SMTP relay attempt failed: {str(exc)}. Recorded in CRM activity trail."
    else:
        sent_successfully = False
        delivery_status_msg = f"Email drafted & logged to CRM activities for {to_email}. (To dispatch to recipient's real inbox, configure SMTP_USER & SMTP_PASSWORD in backend/.env)"

    # Record Activity in CRM Database
    db = SessionLocal()
    activity_id = None
    try:
        activity = Activity(
            type=ActivityType.EMAIL,
            subject=subject[:300],
            description=f"To: {to_email}\nStatus: {'SENT' if sent_successfully else 'LOGGED'}\n\n{body}",
            contact_id=contact_id,
            outcome=delivery_status_msg[:200],
            completed_at=datetime.now(timezone.utc),
            scheduled_at=datetime.now(timezone.utc)
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)
        activity_id = activity.id
    except Exception as exc:
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
        "error": error_detail,
        "smtp_configured": smtp_configured
    }
