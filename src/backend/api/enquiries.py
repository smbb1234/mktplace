from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Body, status
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Any

from src.backend.repositories.leads import LeadsRepository
from src.backend.core.database import get_db
from src.backend.schemas.enquiries import EnquiryCreate, EnquiryResponse

router = APIRouter(prefix="/enquiries", tags=["enquiries"])


def _get_repo(db: Session = Depends(get_db)) -> LeadsRepository:
    return LeadsRepository(db)


@router.post("/", response_model=EnquiryResponse, status_code=status.HTTP_201_CREATED)
def create_enquiry(
    payload: EnquiryCreate, repo: LeadsRepository = Depends(_get_repo)
) -> EnquiryResponse:
    try:
        e = repo.create_enquiry(enquiry_data=payload.dict())
        return EnquiryResponse(
            enquiry_id=e.enquiry_id,
            vehicle_id=e.vehicle_id,
            full_name=e.full_name,
            email=e.email,
            phone=e.phone,
            status=e.status,
            created_at=e.created_at,
        )
    except SQLAlchemyError:
        logging.exception("Database error creating enquiry")
        raise HTTPException(status_code=500, detail="Database error creating enquiry")
    except Exception:
        logging.exception("Failed to create enquiry")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{enquiry_id}", response_model=EnquiryResponse)
def get_enquiry(enquiry_id: str, repo: LeadsRepository = Depends(_get_repo)) -> EnquiryResponse:
    e = repo.get_enquiry(enquiry_id)
    if not e:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    return EnquiryResponse(
        enquiry_id=e.enquiry_id,
        vehicle_id=e.vehicle_id,
        full_name=e.full_name,
        email=e.email,
        phone=e.phone,
        status=e.status,
        created_at=e.created_at,
    )
