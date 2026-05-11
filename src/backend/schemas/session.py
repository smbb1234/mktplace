from __future__ import annotations

from pydantic import BaseModel
from typing import Optional


class SessionCreate(BaseModel):
    session_id: Optional[str] = None


class SessionResponse(BaseModel):
    session_id: str
    stage: str