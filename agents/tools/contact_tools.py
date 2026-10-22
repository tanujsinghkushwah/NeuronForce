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
    notes: str = "",
) -> Dict[str, Any]:
    """Create a new contact record in the CRM."""
    db = SessionLocal()
    try:
        # Check if email exists
        existing = db.query(Contact).filter(Contact.email == email).first()
        if existing:
            full_name = f"{existing.first_name} {existing.last_name}".strip()
            comp_suffix = (
                f" at {existing.company}"
                if existing.company
                and str(existing.company).lower() not in ("null", "none", "unassigned")
                else ""
            )
            return {
                "success": True,
                "action": "create_contact",
                "contact": {
                    "id": existing.id,
                    "name": full_name,
                    "email": existing.email,
                    "company": existing.company or "",
                },
                "message": f"Contact with email '{email}' already exists ({full_name}{comp_suffix}).",
            }

        matched_status = LeadStatus.NEW
        for s in LeadStatus:
            if (
                s.value.lower() == lead_status.lower()
                or s.name.lower() == lead_status.lower()
            ):
                matched_status = s
                break

        clean_company = (
            ""
            if not company or str(company).lower() in ("null", "none", "unassigned")
            else str(company).strip()
        )
        clean_title = (
            ""
            if not job_title or str(job_title).lower() in ("null", "none")
            else str(job_title).strip()
        )

        contact = Contact(
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            email=email.strip(),
            company=clean_company,
            job_title=clean_title,
            phone=phone.strip(),
            lead_status=matched_status,
            lead_score=lead_score,
            notes=notes or f"Created autonomously via Sales Agent Studio",
            avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed={first_name}{last_name}",
        )
        db.add(contact)
        db.commit()
        db.refresh(contact)

        full_name = f"{contact.first_name} {contact.last_name}".strip()
        comp_suffix = f" at {contact.company}" if contact.company else ""
        role_label = (
            f" ({contact.job_title or 'Contact'}{comp_suffix})"
            if (contact.job_title or comp_suffix)
            else ""
        )

        return {
            "success": True,
            "action": "create_contact",
            "contact": {
                "id": contact.id,
                "name": full_name,
                "email": contact.email,
                "company": contact.company or "",
                "job_title": contact.job_title or "",
                "lead_status": contact.lead_status.value,
                "lead_score": contact.lead_score,
            },
            "message": f"Successfully added contact {full_name}{role_label} with email {contact.email}.",
        }
    except Exception as exc:
        db.rollback()
        return {
            "success": False,
            "action": "create_contact",
            "error": str(exc),
            "message": f"Failed to create contact: {str(exc)}",
        }
    finally:
        db.close()


def update_contact(
    identifier: str,  # id or email or name
    email: Optional[str] = None,
    lead_status: Optional[str] = None,
    job_title: Optional[str] = None,
    company: Optional[str] = None,
    notes: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> Dict[str, Any]:
    """Update contact information, email, names, or lead status."""
    db = SessionLocal()
    try:
        contact = None
        ident_str = str(identifier).strip()
        if ident_str.isdigit():
            contact = db.query(Contact).filter(Contact.id == int(ident_str)).first()
        if not contact and "@" in ident_str:
            contact = db.query(Contact).filter(Contact.email.ilike(ident_str)).first()
        if not contact:
            contact = (
                db.query(Contact)
                .filter(
                    (Contact.first_name.ilike(f"%{ident_str}%"))
                    | (Contact.last_name.ilike(f"%{ident_str}%"))
                )
                .first()
            )
        if not contact and " " in ident_str:
            parts = ident_str.split()
            contact = (
                db.query(Contact)
                .filter(
                    (Contact.first_name.ilike(f"%{parts[0]}%"))
                    | (Contact.last_name.ilike(f"%{parts[-1]}%"))
                )
                .first()
            )

        if not contact:
            return {
                "success": False,
                "message": f"Contact matching '{identifier}' was not found in CRM.",
            }

        # Update email if provided and valid
        if email and "@" in email:
            clean_email = email.strip()
            # Check if another contact has this email
            existing_email_contact = (
                db.query(Contact)
                .filter(Contact.email == clean_email, Contact.id != contact.id)
                .first()
            )
            if not existing_email_contact:
                contact.email = clean_email

        if first_name:
            contact.first_name = first_name.strip()
        if last_name:
            contact.last_name = last_name.strip()

        if lead_status:
            for s in LeadStatus:
                if (
                    s.value.lower() == lead_status.lower()
                    or s.name.lower() == lead_status.lower()
                ):
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
                "job_title": contact.job_title,
                "lead_status": contact.lead_status.value,
            },
            "message": f"Updated contact {contact.first_name} {contact.last_name} (Email: {contact.email}, Status: {contact.lead_status.value.title()}).",
        }
    except Exception as exc:
        db.rollback()
        return {
            "success": False,
            "action": "update_contact",
            "error": str(exc),
            "message": f"Failed to update contact: {str(exc)}",
        }
    finally:
        db.close()
