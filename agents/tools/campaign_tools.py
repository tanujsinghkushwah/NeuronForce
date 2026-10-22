"""
Campaign Tools for Autonomous Agents
Creates and manages email marketing campaigns.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

CURRENT_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = CURRENT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.database import SessionLocal
from app.models.campaign import Campaign, CampaignStatus, CampaignType


def create_campaign(
    name: str,
    subject: str,
    type: str = "email",
    preview_text: str = "",
    body_text: str = "",
    target_segment: str = "enterprise_leads",
) -> Dict[str, Any]:
    """Create a new email marketing campaign draft."""
    db = SessionLocal()
    try:
        matched_type = CampaignType.EMAIL
        for t in CampaignType:
            if t.value.lower() == type.lower():
                matched_type = t
                break

        campaign = Campaign(
            name=name,
            type=matched_type,
            status=CampaignStatus.DRAFT,
            subject=subject,
            preview_text=preview_text
            or f"Exclusive update for {target_segment.replace('_', ' ').title()}",
            body_text=body_text
            or f"Hello,\n\nWe are excited to share an exclusive update tailored for {target_segment.replace('_', ' ')}.\n\nBest regards,\nNeuronForce Team",
            body_html=f"<p>Hello,</p><p>We are excited to share an exclusive update tailored for <strong>{target_segment.replace('_', ' ')}</strong>.</p><p>Best regards,<br/>NeuronForce Team</p>",
            audience_filter={"segment": target_segment},
            description=f"Auto-generated campaign created via Autonomous Sales Agent for {target_segment}",
        )
        db.add(campaign)
        db.commit()
        db.refresh(campaign)

        return {
            "success": True,
            "action": "create_campaign",
            "campaign": {
                "id": campaign.id,
                "name": campaign.name,
                "subject": campaign.subject,
                "status": campaign.status.value,
                "type": campaign.type.value,
                "preview_text": campaign.preview_text,
            },
            "message": f"Successfully created campaign '{campaign.name}' with subject '{campaign.subject}' (Status: Draft).",
        }
    except Exception as exc:
        db.rollback()
        return {
            "success": False,
            "action": "create_campaign",
            "error": str(exc),
            "message": f"Failed to create campaign: {str(exc)}",
        }
    finally:
        db.close()
