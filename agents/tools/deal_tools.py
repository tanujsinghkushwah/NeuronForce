"""
Deal & Pipeline Tools for Autonomous Agents
Creates, updates, and manages deals in the CRM pipeline.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional

CURRENT_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = CURRENT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.database import SessionLocal
from app.models.deal import Deal
from app.models.enums import DealStage, Priority


def create_deal(
    title: str,
    value: float,
    company: str,
    stage: str = "prospecting",
    probability: Optional[int] = None,
    priority: str = "medium",
    expected_close_days: int = 30,
) -> Dict[str, Any]:
    """Create a new deal in the CRM pipeline."""
    db = SessionLocal()
    try:
        # Match stage enum safely
        matched_stage = DealStage.PROSPECTING
        for s in DealStage:
            if s.value.lower() == stage.lower() or s.name.lower() == stage.lower():
                matched_stage = s
                break

        # Match priority enum safely
        matched_priority = Priority.MEDIUM
        for p in Priority:
            if (
                p.value.lower() == priority.lower()
                or p.name.lower() == priority.lower()
            ):
                matched_priority = p
                break

        default_prob = {
            DealStage.PROSPECTING: 15,
            DealStage.QUALIFICATION: 30,
            DealStage.PROPOSAL: 60,
            DealStage.NEGOTIATION: 80,
            DealStage.CLOSED_WON: 100,
            DealStage.CLOSED_LOST: 0,
        }.get(matched_stage, 25)

        close_date = datetime.now(timezone.utc) + timedelta(days=expected_close_days)

        deal = Deal(
            title=title,
            value=float(value),
            company=company,
            stage=matched_stage,
            probability=probability if probability is not None else default_prob,
            priority=matched_priority,
            expected_close_date=close_date,
            ai_win_probability=round(
                (probability if probability is not None else default_prob) / 100.0, 2
            ),
            description=f"Auto-generated via Autonomous Sales Agent: Deal for {company} valued at ${value:,.2f}",
        )
        db.add(deal)
        db.commit()
        db.refresh(deal)

        return {
            "success": True,
            "action": "create_deal",
            "deal": {
                "id": deal.id,
                "title": deal.title,
                "value": deal.value,
                "company": deal.company,
                "stage": deal.stage.value,
                "probability": deal.probability,
                "priority": deal.priority.value,
            },
            "message": f"Successfully created deal '{deal.title}' for {deal.company} (${deal.value:,.2f}) in {deal.stage.value.title()} stage.",
        }
    except Exception as exc:
        db.rollback()
        return {
            "success": False,
            "action": "create_deal",
            "error": str(exc),
            "message": f"Failed to create deal: {str(exc)}",
        }
    finally:
        db.close()


def update_deal(
    deal_identifier: str,  # deal id (str/int) or company name / deal title
    stage: Optional[str] = None,
    value: Optional[float] = None,
    probability: Optional[int] = None,
) -> Dict[str, Any]:
    """Update deal stage, value, or probability."""
    db = SessionLocal()
    try:
        deal = None
        if str(deal_identifier).isdigit():
            deal = db.query(Deal).filter(Deal.id == int(deal_identifier)).first()
        if not deal:
            # Search by title or company
            deal = (
                db.query(Deal)
                .filter(
                    (Deal.title.ilike(f"%{deal_identifier}%"))
                    | (Deal.company.ilike(f"%{deal_identifier}%"))
                )
                .first()
            )

        if not deal:
            return {
                "success": False,
                "message": f"Deal matching '{deal_identifier}' was not found in the pipeline.",
            }

        if stage:
            for s in DealStage:
                if s.value.lower() == stage.lower() or s.name.lower() == stage.lower():
                    deal.stage = s
                    break

        if value is not None:
            deal.value = float(value)

        if probability is not None:
            deal.probability = int(probability)
            deal.ai_win_probability = round(probability / 100.0, 2)

        db.commit()
        db.refresh(deal)

        return {
            "success": True,
            "action": "update_deal",
            "deal": {
                "id": deal.id,
                "title": deal.title,
                "value": deal.value,
                "company": deal.company,
                "stage": deal.stage.value,
                "probability": deal.probability,
            },
            "message": f"Updated deal '{deal.title}' ({deal.company}): stage is now {deal.stage.value.title()} (${deal.value:,.2f}, {deal.probability}% probability).",
        }
    except Exception as exc:
        db.rollback()
        return {
            "success": False,
            "action": "update_deal",
            "error": str(exc),
            "message": f"Failed to update deal: {str(exc)}",
        }
    finally:
        db.close()
