from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class EnquiryCreate(BaseModel):
    vehicle_id: str
    full_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    message: Optional[str] = None


class EnquiryRead(EnquiryCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
