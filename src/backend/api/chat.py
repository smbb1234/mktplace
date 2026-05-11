from __future__ import annotations

from fastapi import APIRouter, HTTPException
from src.backend.schemas.chat import ChatMessage, ChatResponse
from src.backend.services.ai.preference_extractor import extract_preferences_from_text
from src.backend.services.ai.conversation_orchestrator import (
    create_or_get_session,
    add_message,
    update_preferences,
    get_preferences,
)

router = APIRouter(prefix="/chat", tags=["chat"])

FUEL_QUICK_REPLIES = ["Petrol", "Diesel", "Hybrid / Electric"]
TRANSMISSION_QUICK_REPLIES = ["Automatic", "Manual"]


def _build_next_reply(preferences: dict) -> tuple[str, list[str] | None]:
    if not preferences.get("monthly_budget"):
        return "What's your monthly budget for the car?", None

    if not preferences.get("fuel_type"):
        return "Great — what fuel type would you prefer?", FUEL_QUICK_REPLIES

    if not preferences.get("transmission"):
        return (
            "Got it. Would you prefer automatic or manual transmission?",
            TRANSMISSION_QUICK_REPLIES,
        )

    if not preferences.get("family_size"):
        return "Thanks — how many people do you usually need seats for?", None

    return (
        "Thanks — I have the key details I need. I'm generating recommendations for you now.",
        None,
    )


@router.post("/message", response_model=ChatResponse)
def post_message(payload: ChatMessage):
    s = create_or_get_session(payload.session_id)
    if not s:
        raise HTTPException(status_code=500, detail="Failed to create session")
    session_id = s["session_id"]
    add_message(session_id, payload.message)
    prefs = extract_preferences_from_text(payload.message)
    update_preferences(session_id, prefs)
    current = get_preferences(session_id)
    reply, quick_replies = _build_next_reply(current)
    return ChatResponse(
        session_id=session_id,
        reply=reply,
        intent=current.get("intent"),
        monthly_budget=current.get("monthly_budget"),
        fuel_type=current.get("fuel_type"),
        transmission=current.get("transmission"),
        family_size=current.get("family_size"),
        quick_replies=quick_replies,
    )
