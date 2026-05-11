from src.backend.services.inventory.csv_loader import load_inventory
import csv
from pathlib import Path


def _write_csv(path, rows, fieldnames):
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def test_csv_loader_handles_malformed_json(tmp_path: Path):
    p = tmp_path / "test.csv"
    # valid row
    rows = [
        {"Car Inventory Data": '{"car_id": "CAR1", "make": "A", "model": "B"}',
         "Pricing Details": '{"price_id": "P1", "car_id": "CAR1", "monthly_from_gbp": 200}'},
        # malformed JSON row
        {"Car Inventory Data": '{"car_id": "CAR2", "make": "C", "model": "D"',
         "Pricing Details": ''},
        # missing fields
        {"Car Inventory Data": '', "Pricing Details": ''},
    ]
    fieldnames = ["Car Inventory Data", "Pricing Details"]
    _write_csv(p, rows, fieldnames)

    vehicles, pricing = load_inventory(p)
    assert any(v.vehicle_id == "CAR1" for v in vehicles)
    assert "CAR1" in pricing
