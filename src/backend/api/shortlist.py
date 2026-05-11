from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src.backend.services.leads.shortlist_service import add_to_shortlist, remove_from_shortlist, list_shortlist

router = APIRouter(prefix="/shortlist", tags=["shortlist"])


@router.post("/add")
def add(session_id: str, vehicle_id: str):
    return {"shortlist": list(add_to_shortlist(session_id, vehicle_id))}


@router.post("/remove")
def remove(session_id: str, vehicle_id: str):
    return {"shortlist": list(remove_from_shortlist(session_id, vehicle_id))}


@router.get("/list")
def list_items(session_id: str):
    return {"shortlist": list(list_shortlist(session_id))}
