from __future__ import annotations

from typing import Dict, Any

from src.backend.repositories.leads import LeadsRepository


def create_enquiry(db, enquiry_data: Dict[str, Any]):
    repo = LeadsRepository(db)
    return repo.create_enquiry(enquiry_data=enquiry_data)
