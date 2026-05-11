from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ChatMessage(BaseModel):
    session_id: Optional[str] = None
    message: str


class PreferenceExtractionResponse(BaseModel):
    intent: Optional[str] = None
    monthly_budget: Optional[float] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    family_size: Optional[int] = None


class ChatResponse(PreferenceExtractionResponse):
    session_id: str
    reply: str
    quick_replies: Optional[list[str]] = None
