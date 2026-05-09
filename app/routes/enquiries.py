from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/enquiries", tags=["enquiries"])


def _to_dict(pydantic_obj: Any) -> dict:
    # support pydantic v2 and v1
    if hasattr(pydantic_obj, "model_dump"):
        return pydantic_obj.model_dump()
    return pydantic_obj.dict()


@router.post("/", response_model=schemas.EnquiryRead, status_code=status.HTTP_201_CREATED)
def create_enquiry(enquiry: schemas.EnquiryCreate, db: Session = Depends(get_db)):
    data = _to_dict(enquiry)
    db_enq = models.Enquiry(**data)
    try:
        db.add(db_enq)
        db.commit()
        db.refresh(db_enq)
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error creating enquiry: {exc}")
    return db_enq


@router.get("/{enquiry_id}", response_model=schemas.EnquiryRead)
def get_enquiry(enquiry_id: int, db: Session = Depends(get_db)):
    enq = db.get(models.Enquiry, enquiry_id)
    if not enq:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    return enq
