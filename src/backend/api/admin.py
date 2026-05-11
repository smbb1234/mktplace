from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import List

from src.backend.core.database import get_db
from src.backend.models.leads import Enquiry
from pathlib import Path


router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/flush_offline")
def flush_offline(x_admin_token: str | None = Header(None)):
    from src.shared.config.settings import get_settings
    settings = get_settings()
    admin_token = getattr(settings, "admin_token", None) or ""
    if admin_token and x_admin_token != admin_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    # run the flush script
    from src.backend.scripts.flush_offline_enquiries import flush_queue
    try:
        flush_queue()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/enquiries", response_model=List[dict])
def list_enquiries(db=Depends(get_db), page: int = 1, limit: int = 50, x_admin_token: str | None = Header(None)):
    # simple admin token check
    from src.shared.config.settings import get_settings
    settings = get_settings()
    admin_token = getattr(settings, "admin_token", None) or ""
    if admin_token and x_admin_token != admin_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        q = db.query(Enquiry).order_by(Enquiry.created_at.desc())
        items = q.offset((page - 1) * limit).limit(limit).all()
        return [
            {"enquiry_id": e.enquiry_id, "full_name": e.full_name, "email": e.email, "status": e.status}
            for e in items
        ]
    except Exception:
        raise HTTPException(status_code=503, detail="Database unavailable")


@router.post("/enquiries/{enquiry_id}/status")
def update_enquiry_status(enquiry_id: str, status: str, db=Depends(get_db), x_admin_token: str | None = Header(None)):
    # auth check
    from src.shared.config.settings import get_settings
    settings = get_settings()
    admin_token = getattr(settings, "admin_token", None) or ""
    if admin_token and x_admin_token != admin_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        e = db.query(Enquiry).filter(Enquiry.enquiry_id == enquiry_id).one_or_none()
        if not e:
            raise HTTPException(status_code=404, detail="Enquiry not found")
        e.status = status
        db.add(e)
        db.commit()
        return {"enquiry_id": enquiry_id, "status": status}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=503, detail="Database unavailable")
