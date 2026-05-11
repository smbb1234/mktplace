from src.backend.services.inventory.catalog import InventoryCatalog
import csv


def _write_sample_csv(path):
    rows = [
        {"Car Inventory Data": '{"car_id": "C1", "make": "X", "model": "One", "fuel_type": "Petrol", "transmission": "Manual"}',
         "Pricing Details": '{"price_id": "P1", "car_id": "C1", "monthly_from_gbp": 250}'},
        {"Car Inventory Data": '{"car_id": "C2", "make": "Y", "model": "Two", "fuel_type": "Diesel", "transmission": "Automatic"}',
         "Pricing Details": '{"price_id": "P2", "car_id": "C2", "monthly_from_gbp": 800}'},
    ]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["Car Inventory Data", "Pricing Details"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def test_catalog_filters_by_budget(tmp_path):
    p = tmp_path / "inv.csv"
    _write_sample_csv(p)
    catalog = InventoryCatalog(csv_path=p)
    catalog.load()
    results = catalog.filter(budget_monthly_max=300)
    assert len(results) == 1
    assert results[0].vehicle_id == "C1"


def test_catalog_filters_by_fuel_and_transmission(tmp_path):
    p = tmp_path / "inv2.csv"
    _write_sample_csv(p)
    catalog = InventoryCatalog(csv_path=p)
    catalog.load()
    results = catalog.filter(fuel_type="Diesel", transmission="Automatic")
    assert len(results) == 1
    assert results[0].vehicle_id == "C2"
