"""
Deals & Pipeline API Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from app.database import get_db
from app.models.deal import Deal
from app.models.contact import Contact
from app.models.enums import DealStage
from app.schemas import DealCreate, DealUpdate, DealResponse

router = APIRouter(prefix="/api/deals", tags=["Deals"])


@router.get("", response_model=List[DealResponse])
def list_deals(
    skip: int = 0,
    limit: int = 50,
    stage: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List deals with optional filtering."""
    query = db.query(Deal)
    if stage:
        query = query.filter(Deal.stage == stage)
    if search:
        query = query.filter(
            (Deal.title.ilike(f"%{search}%")) | (Deal.company.ilike(f"%{search}%"))
        )
    query = query.order_by(desc(Deal.created_at))
    return query.offset(skip).limit(limit).all()


@router.get("/pipeline")
def get_pipeline(db: Session = Depends(get_db)):
    """Get deals organized by pipeline stage."""
    pipeline = {}
    total_value = 0
    weighted_value = 0

    for stage in DealStage:
        deals = (
            db.query(Deal).filter(Deal.stage == stage).order_by(desc(Deal.value)).all()
        )
        pipeline[stage.value] = []
        for d in deals:
            deal_data = {
                "id": d.id,
                "title": d.title,
                "value": d.value,
                "company": d.company,
                "probability": d.probability,
                "owner": d.owner,
                "priority": d.priority.value if d.priority else "medium",
                "expected_close_date": (
                    d.expected_close_date.isoformat() if d.expected_close_date else None
                ),
                "ai_win_probability": d.ai_win_probability,
                "tags": d.tags or [],
                "contacts": [
                    {
                        "id": c.id,
                        "name": f"{c.first_name} {c.last_name}",
                        "avatar_url": c.avatar_url,
                    }
                    for c in d.contacts
                ],
            }
            pipeline[stage.value].append(deal_data)
            if stage not in [DealStage.CLOSED_WON, DealStage.CLOSED_LOST]:
                total_value += d.value or 0
                weighted_value += (d.value or 0) * (d.probability or 0) / 100

    return {
        "stages": pipeline,
        "total_value": total_value,
        "weighted_value": round(weighted_value, 2),
    }


@router.get("/{deal_id}", response_model=DealResponse)
def get_deal(deal_id: int, db: Session = Depends(get_db)):
    """Get a specific deal by ID."""
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.post("", response_model=DealResponse)
def create_deal(deal: DealCreate, db: Session = Depends(get_db)):
    """Create a new deal."""
    deal_data = deal.model_dump(exclude={"contact_ids"})
    db_deal = Deal(**deal_data)
    if deal.contact_ids:
        contacts = db.query(Contact).filter(Contact.id.in_(deal.contact_ids)).all()
        db_deal.contacts = contacts
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    return db_deal


@router.put("/{deal_id}", response_model=DealResponse)
def update_deal(deal_id: int, deal: DealUpdate, db: Session = Depends(get_db)):
    """Update a deal."""
    db_deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not db_deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    update_data = deal.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_deal, key, value)
    db.commit()
    db.refresh(db_deal)
    return db_deal


@router.delete("/{deal_id}")
def delete_deal(deal_id: int, db: Session = Depends(get_db)):
    """Delete a deal."""
    db_deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not db_deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    db.delete(db_deal)
    db.commit()
    return {"message": "Deal deleted"}
