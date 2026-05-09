from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum

from src.backend.models.common import Base


class CustomerSession(Base):
    __tablename__ = "customer_sessions"

    session_id = Column(String, primary_key=True)
    stage = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
