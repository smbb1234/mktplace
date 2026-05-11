"""Normalize sample CSV rows into a clean dataset.csv for MVP."""

import csv
import json
from pathlib import Path


def normalize(input_path: str = "data/datasetSample.csv", output_path: str = "data/dataset.csv"):
    ip = Path(input_path)
    op = Path(output_path)
    if not ip.exists():
        raise FileNotFoundError(ip)
    rows = []
    with ip.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            inv_cell = row.get("Car Inventory Data")
            price_cell = row.get("Pricing Details")
            try:
                inv = json.loads(inv_cell) if inv_cell else {}
            except Exception:
                inv = {}
            try:
                price = json.loads(price_cell) if price_cell else {}
            except Exception:
                price = {}
            # Minimal normalization: ensure car_id and price_id exist
            inv.setdefault("car_id", inv.get("vehicle_id", "UNKNOWN"))
            price.setdefault("price_id", price.get("price_id", "P-UNKNOWN"))
            rows.append({"Car Inventory Data": json.dumps(inv), "Pricing Details": json.dumps(price)})

    with op.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["Car Inventory Data", "Pricing Details"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"Wrote normalized dataset to {op}")


if __name__ == "__main__":
    normalize()
