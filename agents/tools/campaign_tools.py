"""
Campaign Tools for Autonomous Agents
Creates and manages AI-enhanced marketing campaigns across Email, X, and Instagram.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

CURRENT_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = CURRENT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.database import SessionLocal
from app.models.campaign import Campaign, CampaignStatus, CampaignType
from agents.subagents.llm_client import call_llm_json


def generate_ai_campaign_content(
    prompt: str,
    deal_context: Optional[Dict[str, Any]] = None,
    target_channels: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Use LLM to generate targeted, high-converting multi-channel campaign copy
    (Email, X/Twitter, Instagram) referencing the specific deal, stakeholders, and value.
    """
    channels = target_channels or []
    lower_prompt = prompt.lower()
    if not channels:
        if " x" in lower_prompt or "twitter" in lower_prompt:
            channels.append("X")
        if "instagram" in lower_prompt or "ig" in lower_prompt:
            channels.append("Instagram")
        if "linkedin" in lower_prompt:
            channels.append("LinkedIn")
        if not channels:
            channels = ["Email", "X", "Instagram"]

    deal_str = ""
    if deal_context:
        title = deal_context.get("title", "Enterprise Strategic Partnership")
        val = (
            f"${float(deal_context.get('value', 0)):,.2f}"
            if deal_context.get("value")
            else ""
        )
        co = deal_context.get("company", "")
        deal_str = f"Deal: {title} {val} (Account: {co})"

    system_prompt = (
        "You are an elite B2B Growth Marketing Director for NeuronForce. "
        "Generate a creative, high-converting multi-channel campaign announcement. "
        "Explicitly mention the deal, key stakeholders, and dollar scale if provided. "
        "Provide platform-native copy for X (Twitter) and Instagram when requested.\n\n"
        "Return a JSON object with this exact structure:\n"
        "{\n"
        '  "name": "<compelling campaign name>",\n'
        '  "subject": "<high-open-rate subject line>",\n'
        '  "preview_text": "<preview snippet under 100 chars>",\n'
        '  "target_segment": "<e.g. enterprise_stakeholders, high_net_worth>",\n'
        '  "x_post": "<punchy, engaging post for X with 2-3 hashtags>",\n'
        '  "instagram_caption": "<visually driven Instagram caption with storytelling and call to action>",\n'
        '  "body_text": "<multi-paragraph announcement body>"\n'
        "}"
    )

    user_prompt = (
        f"User Request: {prompt}\nTarget Channels: {', '.join(channels)}\n{deal_str}"
    )
    res = call_llm_json(system_prompt, user_prompt)

    if res and isinstance(res.get("data"), dict):
        data = res["data"]
        data["channels"] = channels
        return data

    # High-quality fallback if LLM is offline
    deal_title = (
        deal_context.get("title") if deal_context else "Strategic Enterprise Deal"
    )
    val_snippet = (
        f" worth ${float(deal_context.get('value', 0)):,.2f}"
        if deal_context and deal_context.get("value")
        else ""
    )

    return {
        "name": f"Campaign: {deal_title}",
        "subject": f"🚀 Strategic Milestone: Expanding {deal_title}{val_snippet}",
        "preview_text": f"Exciting enterprise expansion and partnership updates on {deal_title}.",
        "target_segment": "enterprise_executives",
        "channels": channels,
        "x_post": f"Thrilled to announce significant momentum with {deal_title}{val_snippet}! Scaling autonomous sales operations with our valued partners. 🚀 #EnterpriseGrowth #SalesAI #NeuronForce",
        "instagram_caption": f"Big milestones in the making ✨\n\nCelebrating rapid momentum on {deal_title}{val_snippet}. Transforming how high-performing revenue teams orchestrate deals with autonomous AI.\n\n🔗 Link in bio to learn more.\n\n#SalesTech #AIInnovation #EnterprisePartnership #NeuronForce",
        "body_text": f"We are thrilled to announce our latest milestone regarding {deal_title}{val_snippet}.\n\nThis campaign highlights our collaborative enterprise transformation, driving autonomous intelligence across modern sales pipelines.",
    }


def create_campaign(
    name: str,
    subject: str,
    type: str = "promotional",
    preview_text: str = "",
    body_text: str = "",
    target_segment: str = "enterprise_leads",
    channels: Optional[List[str]] = None,
    social_copy: Optional[Dict[str, str]] = None,
    deal_id: Optional[int] = None,
) -> Dict[str, Any]:
    """Create a new AI-enhanced marketing campaign draft in the CRM."""
    db = SessionLocal()
    try:
        matched_type = CampaignType.PROMOTIONAL
        for t in CampaignType:
            if t.value.lower() == type.lower():
                matched_type = t
                break

        full_desc = f"AI-orchestrated multi-channel campaign for {target_segment}."
        if channels:
            full_desc += f" Channels: {', '.join(channels)}."

        audience_meta: Dict[str, Any] = {
            "segment": target_segment,
            "channels": channels or ["email"],
        }
        if social_copy:
            audience_meta["social_copy"] = social_copy
        if deal_id:
            audience_meta["deal_id"] = deal_id

        campaign = Campaign(
            name=name,
            type=matched_type,
            status=CampaignStatus.DRAFT,
            subject=subject,
            preview_text=preview_text
            or f"Exclusive update for {target_segment.replace('_', ' ').title()}",
            body_text=body_text
            or f"Hello,\n\nWe are excited to share an exclusive update tailored for {target_segment.replace('_', ' ')}.\n\nBest regards,\nNeuronForce Team",
            body_html=f"<p>{body_text.replace(chr(10), '<br/>') if body_text else 'Hello,<br/>Exclusive update.'}</p>",
            audience_filter=audience_meta,
            description=full_desc,
        )
        db.add(campaign)
        db.commit()
        db.refresh(campaign)

        campaign_data = {
            "id": campaign.id,
            "name": campaign.name,
            "subject": campaign.subject,
            "status": campaign.status.value,
            "type": campaign.type.value,
            "preview_text": campaign.preview_text,
            "channels": channels or ["email"],
            "social_copy": social_copy or {},
        }

        channel_str = f" on {', '.join(channels)}" if channels else ""
        return {
            "success": True,
            "action": "create_campaign",
            "campaign": campaign_data,
            "message": f"Successfully created AI-enhanced campaign '{campaign.name}'{channel_str} with subject '{campaign.subject}' (Status: Draft).",
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
