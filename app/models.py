from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from .database import Base


class Enquiry(Base):
    __tablename__ = "enquiries"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String(64), nullable=False, index=True)
    full_name = Column(String(128), nullable=False)
    email = Column(String(256), nullable=True)
    phone = Column(String(64), nullable=True)
    message = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
