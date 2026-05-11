from __future__ import annotations

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class VehiclePricing(BaseModel):
    price_id: str
    vehicle_id: str = Field(..., alias="car_id")
    list_price_gbp: Optional[float] = None
    monthly_from_gbp: Optional[float] = None
    deposit_gbp: Optional[float] = None
    apr_percent: Optional[float] = None
    term_months: Optional[int] = None
    annual_mileage_limit: Optional[int] = None
    admin_fee_gbp: Optional[float] = None
    delivery_fee_gbp: Optional[float] = None
    discount_gbp: Optional[float] = None
    vat_included: Optional[bool] = None
    price_updated_at: Optional[datetime] = None


class InventoryVehicle(BaseModel):
    vehicle_id: str = Field(..., alias="car_id")
    make: str
    model: Optional[str] = None
    variant: Optional[str] = None
    body_type: Optional[str] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    registration_year: Optional[int] = None
    mileage: Optional[int] = None
    colour: Optional[str] = None
    doors: Optional[int] = None
    seats: Optional[int] = None
    location: Optional[str] = None
    stock_status: Optional[str] = None
    is_featured: Optional[bool] = None
    added_date: Optional[datetime] = None

    def display_title(self) -> str:
        parts = [self.make or "", self.model or ""]
        if self.variant:
            parts.append(self.variant)
        return " ".join([p for p in parts if p])
