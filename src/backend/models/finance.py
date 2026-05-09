from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text

from src.backend.models.common import Base


class FinanceEstimate(Base):
    __tablename__ = "finance_estimates"

    estimate_id = Column(String, primary_key=True)
    session_id = Column(String, nullable=True)
    vehicle_id = Column(String, nullable=False)
    list_price_gbp = Column(Float, nullable=False)
    deposit_gbp = Column(Float, nullable=False)
    term_months = Column(Integer, nullable=False)
    apr_percent = Column(Float, nullable=False)
    estimated_monthly_gbp = Column(Float, nullable=False)
    disclaimer_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
