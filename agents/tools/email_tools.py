"""
Email Dispatch Tool for Autonomous Sales Agents
Wraps the centralized email service for outbound delivery and CRM activity logging.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

CURRENT_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = CURRENT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

try:
    from app.services.email_service import send_email_message as _send_email_message
except ImportError:
    # Fallback if app is in backend namespace
    from backend.app.services.email_service import send_email_message as _send_email_message


def send_email_message(
    to_email: str,
    subject: str,
    body: str,
    to_name: Optional[str] = None,
    contact_id: Optional[int] = None,
    html_body: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Dispatch an outbound email via Resend or SMTP and record in CRM Activity trail.
    """
    return _send_email_message(
        to_email=to_email,
        subject=subject,
        body=body,
        to_name=to_name,
        contact_id=contact_id,
        html_body=html_body,
    )
