"""Seed demo enquiries into the local database for walkthroughs."""

from __future__ import annotations

import json
from pathlib import Path
from src.backend.core.database import engine, SessionLocal
from src.backend.models.common import Base
from src.backend.services.inventory.csv_loader import load_inventory
from src.backend.repositories.leads import LeadsRepository


def seed_demo_enquiries(csv_path: Path | str = "data/datasetSample.csv") -> None:
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    vehicles, pricing = load_inventory(csv_path)
    if not vehicles:
        print("No vehicles found in CSV; nothing to seed.")
        return

    first_vid = vehicles[0].vehicle_id

    session = SessionLocal()
    repo = LeadsRepository(session)
    demo_enquiries = [
        {
            "vehicle_id": first_vid,
            "full_name": "Demo User",
            "email": "demo.user@example.com",
            "phone": "+447700900001",
            "monthly_budget_gbp": 300,
            "deposit_gbp": 1000,
            "buying_timeframe": "1-3 months",
        },
        {
            "vehicle_id": first_vid,
            "full_name": "Sample Lead",
            "email": "sample.lead@example.com",
            "phone": "+447700900002",
            "monthly_budget_gbp": 400,
            "deposit_gbp": 1200,
            "buying_timeframe": "ASAP",
        },
    ]

    for dq in demo_enquiries:
        e = repo.create_enquiry(enquiry_data=dq)
        print("Created enquiry:", e.enquiry_id)

    session.close()


if __name__ == "__main__":
    seed_demo_enquiries()
