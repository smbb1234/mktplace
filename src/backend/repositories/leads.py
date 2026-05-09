from __future__ import annotations

from typing import List, Optional
from uuid import uuid4
from sqlalchemy.orm import Session

from src.backend.models.leads import Enquiry, LeadNote
import logging


class LeadsRepository:
    """Repository for enquiries and lead notes.

    Methods accept a SQLAlchemy `Session` so callers control transactions.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_enquiry(self, *, enquiry_data: dict) -> Enquiry:
        if not enquiry_data.get("enquiry_id"):
            enquiry_data["enquiry_id"] = str(uuid4())
        try:
            enquiry = Enquiry(**enquiry_data)
            self.db.add(enquiry)
            self.db.flush()
            return enquiry
        except Exception as exc:
            logging.exception("Failed to create enquiry with payload: %s", enquiry_data)
            raise

    def get_enquiry(self, enquiry_id: str) -> Optional[Enquiry]:
        return self.db.query(Enquiry).filter(Enquiry.enquiry_id == enquiry_id).one_or_none()

    def list_enquiries(self, *, status: Optional[str] = None, limit: int = 100) -> List[Enquiry]:
        q = self.db.query(Enquiry)
        if status:
            q = q.filter(Enquiry.status == status)
        return q.order_by(Enquiry.created_at.desc()).limit(limit).all()

    def add_note(self, *, enquiry_id: str, note_text: str) -> LeadNote:
        note = LeadNote(note_id=str(uuid4()), enquiry_id=enquiry_id, note_text=note_text)
        self.db.add(note)
        self.db.flush()
        return note
