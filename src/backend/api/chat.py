from __future__ import annotations

from fastapi import APIRouter, HTTPException
from src.backend.schemas.chat import ChatMessage, ChatResponse
from src.backend.services.ai.preference_extractor import extract_preferences_from_text
from src.backend.services.inventory.catalog import get_default_catalog
from src.backend.services.ai.conversation_orchestrator import (
    create_or_get_session,
    add_message,
    update_preferences,
    get_preferences,
    set_last_question_key,
    get_last_question_key,
)

router = APIRouter(prefix="/chat", tags=["chat"])

def _catalog_options(field_name: str) -> list[str]:
    try:
        catalog = get_default_catalog()
        values = {
            str(getattr(vehicle, field_name)).strip()
            for vehicle in catalog.vehicles.values()
            if getattr(vehicle, field_name, None)
        }
    except Exception:
        return []
    return sorted(values)


def _build_next_reply(preferences: dict) -> tuple[str, list[str] | None, str | None]:
    if not preferences.get("monthly_budget"):
        return "Hi! Great to meet you. To begin, what monthly budget feels comfortable?", None, "monthly_budget"

    if not preferences.get("fuel_type"):
        fuel_options = _catalog_options("fuel_type")
        return "Nice — what fuel type would you like?", fuel_options or None, "fuel_type"

    if not preferences.get("body_type"):
        body_options = _catalog_options("body_type")
        return "Great choice. What body style suits you best?", body_options or None, "body_type"

    if not preferences.get("transmission"):
        transmission_options = _catalog_options("transmission")
        return "Perfect. Do you prefer automatic or manual transmission?", transmission_options or None, "transmission"

    if not preferences.get("family_size"):
        return "How many seats do you usually need?", None, "family_size"

    return (
        "Awesome — I have enough to start matching cars. I’ll keep refining with a couple more questions if needed.",
        None,
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
    existing = get_preferences(session_id)
    last_question_key = get_last_question_key(session_id)
    # Context-aware fallback: if the assistant is collecting seats and the
    # user replies with just a number (e.g., "5"), treat it as family size.
    if (
        "family_size" not in prefs
        and existing.get("family_size") is None
        and (existing.get("transmission") or last_question_key == "family_size")
    ):
        stripped = payload.message.strip()
        if stripped.isdigit():
            value = int(stripped)
            if 1 <= value <= 9:
                prefs["family_size"] = value
    update_preferences(session_id, prefs)
    current = get_preferences(session_id)
    reply, quick_replies, next_question_key = _build_next_reply(current)
    set_last_question_key(session_id, next_question_key)
    return ChatResponse(
        session_id=session_id,
        reply=reply,
        intent=current.get("intent"),
        monthly_budget=current.get("monthly_budget"),
        fuel_type=current.get("fuel_type"),
        body_type=current.get("body_type"),
        transmission=current.get("transmission"),
        family_size=current.get("family_size"),
        quick_replies=quick_replies,
    )
