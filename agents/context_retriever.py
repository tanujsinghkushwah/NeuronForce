"""
NeuronForce Context Retriever
Extracts relevant contacts, deals, events, campaigns, and account data from the local CRM database
based on the user's prompt entities.
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, List

# Ensure backend directory is in sys.path
CURRENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = CURRENT_DIR.parent
BACKEND_DIR = REPO_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

try:
    from app.database import SessionLocal
    from app.models.contact import Contact
    from app.models.deal import Deal
    from app.models.calendar import CalendarEvent
    from app.models.campaign import Campaign
except Exception as e:
    # Graceful fallback if database models are loading in isolated mode
    SessionLocal = None
    Contact = None
    Deal = None
    CalendarEvent = None
    Campaign = None


def retrieve_crm_context(prompt: str) -> Dict[str, Any]:
    """
    Search database for entities mentioned in the prompt (names, companies, keywords).
    Returns structured context for the orchestrator and subagents.
    """
    context: Dict[str, Any] = {
        "matching_contacts": [],
        "matching_deals": [],
        "upcoming_events": [],
        "recent_campaigns": [],
        "summary": "No matching records found in CRM database."
    }

    if not SessionLocal:
        return context

    db = SessionLocal()
    try:
        lower_prompt = prompt.lower()

        # 1. Query Contacts
        all_contacts = db.query(Contact).all()
        matching_contacts = []
        for c in all_contacts:
            full_name = f"{c.first_name} {c.last_name}".lower()
            first_name = c.first_name.lower() if c.first_name else ""
            last_name = c.last_name.lower() if c.last_name else ""
            company = c.company.lower() if c.company else ""

            if (first_name and first_name in lower_prompt) or \
               (last_name and last_name in lower_prompt) or \
               (full_name in lower_prompt) or \
               (company and company in lower_prompt):
                matching_contacts.append({
                    "id": c.id,
                    "name": f"{c.first_name} {c.last_name}",
                    "email": c.email,
                    "phone": c.phone,
                    "company": c.company,
                    "job_title": c.job_title,
                    "lead_status": c.lead_status.value if hasattr(c.lead_status, "value") else str(c.lead_status),
                    "lead_score": c.lead_score,
                    "notes": c.notes,
                })

        # If no specific contact matched, grab top 3 active contacts as contextual background
        if not matching_contacts and all_contacts:
            matching_contacts = [
                {
                    "id": c.id,
                    "name": f"{c.first_name} {c.last_name}",
                    "email": c.email,
                    "company": c.company,
                    "job_title": c.job_title,
                    "lead_status": c.lead_status.value if hasattr(c.lead_status, "value") else str(c.lead_status),
                    "lead_score": c.lead_score,
                }
                for c in all_contacts[:3]
            ]
        context["matching_contacts"] = matching_contacts

        # 2. Query Deals
        all_deals = db.query(Deal).all()
        matching_deals = []
        for d in all_deals:
            title = d.title.lower() if d.title else ""
            company = d.company.lower() if d.company else ""
            if (title and any(word in lower_prompt for word in title.split() if len(word) > 3)) or \
               (company and company in lower_prompt):
                matching_deals.append({
                    "id": d.id,
                    "title": d.title,
                    "value": d.value,
                    "stage": d.stage.value if hasattr(d.stage, "value") else str(d.stage),
                    "company": d.company,
                    "probability": d.probability,
                    "ai_win_probability": d.ai_win_probability,
                })

        if not matching_deals and all_deals:
            matching_deals = [
                {
                    "id": d.id,
                    "title": d.title,
                    "value": d.value,
                    "stage": d.stage.value if hasattr(d.stage, "value") else str(d.stage),
                    "company": d.company,
                    "probability": d.probability,
                }
                for d in all_deals[:5]
            ]
        context["matching_deals"] = matching_deals

        # Compute Aggregate Pipeline Metrics for general queries and analytics
        total_deals_count = len(all_deals)
        total_pipeline_val = sum(float(d.value or 0) for d in all_deals)
        deals_by_stage: Dict[str, Dict[str, Any]] = {}
        for d in all_deals:
            stg = d.stage.value if hasattr(d.stage, "value") else str(d.stage)
            if stg not in deals_by_stage:
                deals_by_stage[stg] = {"count": 0, "total_value": 0.0}
            deals_by_stage[stg]["count"] += 1
            deals_by_stage[stg]["total_value"] += float(d.value or 0)

        context["pipeline_metrics"] = {
            "total_deals_count": total_deals_count,
            "total_pipeline_value": total_pipeline_val,
            "deals_by_stage": deals_by_stage,
            "total_contacts_count": len(all_contacts),
            "total_events_count": len(db.query(CalendarEvent).all()),
            "all_deals_overview": [
                {
                    "title": d.title,
                    "company": d.company,
                    "value": d.value,
                    "stage": d.stage.value if hasattr(d.stage, "value") else str(d.stage),
                    "probability": d.probability,
                }
                for d in all_deals
            ]
        }

        # 3. Query Calendar Events
        events = db.query(CalendarEvent).order_by(CalendarEvent.start_time.asc()).limit(5).all()
        context["upcoming_events"] = [
            {
                "id": e.id,
                "title": e.title,
                "start_time": e.start_time.isoformat() if e.start_time else None,
                "end_time": e.end_time.isoformat() if e.end_time else None,
                "attendees": e.attendees or [],
                "location": e.location,
            }
            for e in events
        ]

        # 4. Query Campaigns
        campaigns = db.query(Campaign).order_by(Campaign.id.desc()).limit(3).all()
        context["recent_campaigns"] = [
            {
                "id": cmp.id,
                "name": cmp.name,
                "type": cmp.type.value if hasattr(cmp.type, "value") else str(cmp.type),
                "status": cmp.status.value if hasattr(cmp.status, "value") else str(cmp.status),
                "subject": cmp.subject,
            }
            for cmp in campaigns
        ]

        # Context summary string
        c_names = [c["name"] for c in matching_contacts]
        d_titles = [d["title"] for d in matching_deals]
        context["summary"] = (
            f"CRM Pipeline: {total_deals_count} active deals totaling ${total_pipeline_val:,.2f}. "
            f"Found {len(matching_contacts)} contacts ({', '.join(c_names[:3])}), {len(matching_deals)} deals ({', '.join(d_titles[:2])}), {len(context['upcoming_events'])} calendar events."
        )

    except Exception as exc:
        context["summary"] = f"Context extraction completed with error: {str(exc)}"
    finally:
        db.close()

    return context

