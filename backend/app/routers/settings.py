"""
Application Settings API Router
"""

from fastapi import APIRouter

router = APIRouter(prefix="/api/settings", tags=["Settings"])


@router.get("")
def get_settings():
    """Get application configuration and settings."""
    return {
        "company": {
            "name": "NeuronForce",
            "timezone": "America/Los_Angeles",
            "currency": "USD",
            "fiscal_year_start": "January",
        },
        "ai_config": {
            "auto_lead_scoring": True,
            "auto_email_drafts": True,
            "churn_prediction_enabled": True,
            "forecast_model": "ensemble",
            "max_daily_budget": 5.00,
            "confidence_threshold": 0.7,
            "model_provider": "multi-model",
            "cost_optimization": True,
        },
        "notifications": {
            "email_alerts": True,
            "deal_stage_changes": True,
            "ai_task_completion": True,
            "daily_digest": True,
        },
        "pipeline_stages": [
            {"key": "prospecting", "label": "Prospecting", "probability": 10},
            {"key": "qualification", "label": "Qualification", "probability": 25},
            {"key": "proposal", "label": "Proposal", "probability": 50},
            {"key": "negotiation", "label": "Negotiation", "probability": 75},
            {"key": "closed_won", "label": "Closed Won", "probability": 100},
            {"key": "closed_lost", "label": "Closed Lost", "probability": 0},
        ],
    }
