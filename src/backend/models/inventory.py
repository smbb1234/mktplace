from __future__ import annotations

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class VehiclePricing(BaseModel):
    price_id: str
    vehicle_id: str = Field(..., alias="car_id")
    list_price_gbp: Optional[float]
    monthly_from_gbp: Optional[float]
    deposit_gbp: Optional[float]
    apr_percent: Optional[float]
    term_months: Optional[int]
    annual_mileage_limit: Optional[int]
    admin_fee_gbp: Optional[float]
    delivery_fee_gbp: Optional[float]
    discount_gbp: Optional[float]
    vat_included: Optional[bool]
    price_updated_at: Optional[datetime]


class InventoryVehicle(BaseModel):
    vehicle_id: str = Field(..., alias="car_id")
    make: str
    model: str
    variant: Optional[str]
    body_type: Optional[str]
    fuel_type: Optional[str]
    transmission: Optional[str]
    registration_year: Optional[int]
    mileage: Optional[int]
    colour: Optional[str]
    doors: Optional[int]
    seats: Optional[int]
    location: Optional[str]
    stock_status: Optional[str]
    is_featured: Optional[bool]
    added_date: Optional[datetime]

    def display_title(self) -> str:
        parts = [self.make or "", self.model or ""]
        if self.variant:
            parts.append(self.variant)
        return " ".join([p for p in parts if p])
