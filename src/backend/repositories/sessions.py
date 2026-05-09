from __future__ import annotations

from typing import Optional
from uuid import uuid4
from sqlalchemy.orm import Session

from src.backend.models.session import CustomerSession


class SessionsRepository:
    """Repository for customer sessions."""

    def __init__(self, db: Session):
        self.db = db

    def create_session(self, *, session_id: Optional[str] = None, stage: str = "start") -> CustomerSession:
        if not session_id:
            session_id = str(uuid4())
        s = CustomerSession(session_id=session_id, stage=stage)
        self.db.add(s)
        self.db.flush()
        return s

    def get_session(self, session_id: str) -> Optional[CustomerSession]:
        return self.db.query(CustomerSession).filter(CustomerSession.session_id == session_id).one_or_none()

    def update_stage(self, session_id: str, new_stage: str) -> Optional[CustomerSession]:
        s = self.get_session(session_id)
        if not s:
            return None
        s.stage = new_stage
        self.db.add(s)
        self.db.flush()
        return s
