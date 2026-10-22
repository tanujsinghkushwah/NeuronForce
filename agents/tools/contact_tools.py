"""
Contact Tools for Autonomous Agents
Creates, updates, and retrieves contacts in the CRM.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

CURRENT_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = CURRENT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.database import SessionLocal
from app.models.contact import Contact
from app.models.enums import LeadStatus


def create_contact(
    first_name: str,
    last_name: str,
    email: str,
    company: str = "",
    job_title: str = "",
    phone: str = "",
    lead_status: str = "new",
    lead_score: int = 50,
    notes: str = ""
) -> Dict[str, Any]:
    """Create a new contact record in the CRM."""
    db = SessionLocal()
    try:
        # Check if email exists
        existing = db.query(Contact).filter(Contact.email == email).first()
        if existing:
            return {
                "success": True,
                "action": "create_contact",
                "contact": {
                    "id": existing.id,
                    "name": f"{existing.first_name} {existing.last_name}",
                    "email": existing.email,
                    "company": existing.company,
                },
                "message": f"Contact with email '{email}' already exists ({existing.first_name} {existing.last_name} at {existing.company})."
            }

        matched_status = LeadStatus.NEW
        for s in LeadStatus:
            if s.value.lower() == lead_status.lower() or s.name.lower() == lead_status.lower():
                matched_status = s
                break

        contact = Contact(
            first_name=first_name,
            last_name=last_name,
            email=email,
            company=company,
            job_title=job_title,
            phone=phone,
            lead_status=matched_status,
            lead_score=lead_score,
            notes=notes or f"Created autonomously via Sales Agent Studio",
            avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed={first_name}{last_name}"
        )
        db.add(contact)
        db.commit()
        db.refresh(contact)

        return {
            "success": True,
            "action": "create_contact",
            "contact": {
                "id": contact.id,
                "name": f"{contact.first_name} {contact.last_name}",
                "email": contact.email,
                "company": contact.company,
                "job_title": contact.job_title,
                "lead_status": contact.lead_status.value,
                "lead_score": contact.lead_score,
            },
            "message": f"Successfully added contact {contact.first_name} {contact.last_name} ({contact.job_title or 'Contact'} at {contact.company or 'Unassigned'}) with email {contact.email}."
        }
    except Exception as exc:
        db.rollback()
        return {"success": False, "action": "create_contact", "error": str(exc), "message": f"Failed to create contact: {str(exc)}"}
    finally:
        db.close()


def update_contact(
    identifier: str,  # id or email or name
    lead_status: Optional[str] = None,
    job_title: Optional[str] = None,
    company: Optional[str] = None,
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """Update contact information or lead status."""
    db = SessionLocal()
    try:
        contact = None
        if str(identifier).isdigit():
            contact = db.query(Contact).filter(Contact.id == int(identifier)).first()
        if not contact and "@" in identifier:
            contact = db.query(Contact).filter(Contact.email.ilike(identifier.strip())).first()
        if not contact:
            contact = db.query(Contact).filter(
                (Contact.first_name.ilike(f"%{identifier}%")) |
                (Contact.last_name.ilike(f"%{identifier}%"))
            ).first()

        if not contact:
            return {"success": False, "message": f"Contact matching '{identifier}' was not found in CRM."}

        if lead_status:
            for s in LeadStatus:
                if s.value.lower() == lead_status.lower() or s.name.lower() == lead_status.lower():
                    contact.lead_status = s
                    break

        if job_title:
            contact.job_title = job_title
        if company:
            contact.company = company
        if notes:
            contact.notes = (contact.notes or "") + f"\n[Agent Update]: {notes}"

        db.commit()
        db.refresh(contact)

        return {
            "success": True,
            "action": "update_contact",
            "contact": {
                "id": contact.id,
                "name": f"{contact.first_name} {contact.last_name}",
                "email": contact.email,
                "company": contact.company,
                "lead_status": contact.lead_status.value,
            },
            "message": f"Updated contact {contact.first_name} {contact.last_name} (Status: {contact.lead_status.value.title()})."
        }
    except Exception as exc:
        db.rollback()
        return {"success": False, "action": "update_contact", "error": str(exc), "message": f"Failed to update contact: {str(exc)}"}
    finally:
        db.close()
