from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text

from src.backend.models.common import Base


class Enquiry(Base):
    __tablename__ = "enquiries"

    enquiry_id = Column(String, primary_key=True)
    session_id = Column(String, nullable=True)
    vehicle_id = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    preferred_contact_method = Column(String, nullable=True)
    preferred_contact_time = Column(String, nullable=True)
    monthly_budget_gbp = Column(Integer, nullable=True)
    deposit_gbp = Column(Integer, nullable=True)
    buying_timeframe = Column(String, nullable=True)
    status = Column(String, default="New")
    created_at = Column(DateTime, default=datetime.utcnow)


class LeadNote(Base):
    __tablename__ = "lead_notes"

    note_id = Column(String, primary_key=True)
    enquiry_id = Column(String, nullable=False)
    note_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
