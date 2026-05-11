from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class EnquiryCreate(BaseModel):
    vehicle_id: str
    full_name: str
    email: EmailStr
    phone: str
    preferred_contact_method: Optional[str] = None
    preferred_contact_time: Optional[str] = None
    monthly_budget_gbp: Optional[int] = None
    deposit_gbp: Optional[int] = None
    buying_timeframe: Optional[str] = None


class EnquiryResponse(BaseModel):
    enquiry_id: str
    vehicle_id: str
    full_name: str
    email: EmailStr
    phone: str
    status: str
    created_at: Optional[datetime] = None
