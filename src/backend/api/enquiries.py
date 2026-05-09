from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Body
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Any

from src.backend.repositories.leads import LeadsRepository
from src.backend.core.database import get_db

router = APIRouter(prefix="/enquiries", tags=["enquiries"])


def _get_repo(db: Session = Depends(get_db)) -> LeadsRepository:
    return LeadsRepository(db)


@router.post("/", response_model=dict)
def create_enquiry(
    payload: dict[str, Any] = Body(...), repo: LeadsRepository = Depends(_get_repo)
) -> dict:
    # Basic required-field validation to avoid DB integrity errors
    required = ["vehicle_id", "full_name", "email", "phone"]
    missing = [f for f in required if f not in payload or not payload.get(f)]
    if missing:
        raise HTTPException(status_code=400, detail={"missing_fields": missing})

    try:
        e = repo.create_enquiry(enquiry_data=payload)
        return {"enquiry_id": e.enquiry_id}
    except SQLAlchemyError as exc:
        logging.exception("Database error creating enquiry")
        raise HTTPException(status_code=500, detail="Database error creating enquiry")
    except Exception as exc:
        logging.exception("Failed to create enquiry")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/{enquiry_id}", response_model=dict)
def get_enquiry(enquiry_id: str, repo: LeadsRepository = Depends(_get_repo)) -> dict:
    e = repo.get_enquiry(enquiry_id)
    if not e:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    return {
        "enquiry_id": e.enquiry_id,
        "vehicle_id": e.vehicle_id,
        "full_name": e.full_name,
        "email": e.email,
        "phone": e.phone,
        "status": e.status,
        "created_at": e.created_at.isoformat() if e.created_at else None,
    }
