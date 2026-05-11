from __future__ import annotations

from fastapi.testclient import TestClient

from src.backend.main import app
from src.backend.models.inventory import VehiclePricing

client = TestClient(app)


class FinanceCatalog:
    def __init__(self):
        self._pricing = {
            "vehicle-1": VehiclePricing(
                price_id="price-1",
                car_id="vehicle-1",
                list_price_gbp=24000,
                monthly_from_gbp=410,
                apr_percent=6.0,
                term_months=36,
            )
        }

    def get_pricing(self, vehicle_id: str):
        return self._pricing.get(vehicle_id)


def test_finance_estimate_returns_estimate_for_valid_vehicle_id(monkeypatch):
    monkeypatch.setattr("src.backend.api.finance.get_catalog", lambda: FinanceCatalog())

    response = client.get(
        "/finance/estimate",
        params={"vehicle_id": "vehicle-1", "deposit": 4000, "term_months": 48},
    )

    assert response.status_code == 200
    body = response.json()
    assert "estimate" in body
    assert body["estimate"]["principal"] == 20000
    assert body["estimate"]["monthly"] > 0
    assert body["disclaimer"]


def test_finance_estimate_returns_404_for_unknown_vehicle_id(monkeypatch):
    monkeypatch.setattr("src.backend.api.finance.get_catalog", lambda: FinanceCatalog())

    response = client.get("/finance/estimate", params={"vehicle_id": "missing"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Pricing not found for vehicle"


def test_finance_estimate_returns_503_when_catalog_not_loaded(monkeypatch):
    monkeypatch.setattr("src.backend.api.finance.get_catalog", lambda: None)

    response = client.get("/finance/estimate", params={"vehicle_id": "vehicle-1"})

    assert response.status_code == 503
    assert response.json()["detail"] == "Catalog not loaded"
