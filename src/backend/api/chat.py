from __future__ import annotations

from fastapi import APIRouter, HTTPException
from src.backend.schemas.chat import ChatMessage, PreferenceExtractionResponse
from src.backend.services.ai.preference_extractor import extract_preferences_from_text
from src.backend.services.ai.conversation_orchestrator import (
    create_or_get_session,
    add_message,
    update_preferences,
    get_preferences,
)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/message", response_model=PreferenceExtractionResponse)
def post_message(payload: ChatMessage):
    s = create_or_get_session(payload.session_id)
    if not s:
        raise HTTPException(status_code=500, detail="Failed to create session")
    add_message(s["session_id"], payload.message)
    prefs = extract_preferences_from_text(payload.message)
    update_preferences(s["session_id"], prefs)
    current = get_preferences(s["session_id"])
    return PreferenceExtractionResponse(
        intent=current.get("intent"),
        monthly_budget=current.get("monthly_budget"),
        fuel_type=current.get("fuel_type"),
        transmission=current.get("transmission"),
        family_size=current.get("family_size"),
    )
