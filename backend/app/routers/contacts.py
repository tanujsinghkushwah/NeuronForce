"""
Contacts API Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from app.database import get_db
from app.models.contact import Contact
from app.schemas import ContactCreate, ContactUpdate, ContactResponse

router = APIRouter(prefix="/api/contacts", tags=["Contacts"])


@router.get("", response_model=List[ContactResponse])
def list_contacts(
    skip: int = 0,
    limit: int = 50,
    search: Optional[str] = None,
    status: Optional[str] = None,
    sort_by: Optional[str] = "created_at",
    db: Session = Depends(get_db)
):
    """List contacts with optional filtering and search."""
    query = db.query(Contact)
    if search:
        query = query.filter(
            (Contact.first_name.ilike(f"%{search}%")) |
            (Contact.last_name.ilike(f"%{search}%")) |
            (Contact.email.ilike(f"%{search}%")) |
            (Contact.company.ilike(f"%{search}%"))
        )
    if status:
        query = query.filter(Contact.lead_status == status)
    query = query.order_by(desc(Contact.created_at))
    return query.offset(skip).limit(limit).all()


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """Get a specific contact by ID."""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.post("", response_model=ContactResponse)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    """Create a new contact."""
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    """Update a contact."""
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    update_data = contact.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """Delete a contact."""
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact deleted"}
