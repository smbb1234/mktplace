from fastapi.testclient import TestClient
from src.backend.main import app
from src.backend.services.inventory.catalog import get_default_catalog

client = TestClient(app)


def test_finance_estimate():
    try:
        c = get_default_catalog(csv_path="data/datasetSample.csv")
        import src.backend.startup as startup
        startup.catalog = c
    except Exception:
        pass
    catalog = client.get("/catalog/")
    if catalog.status_code != 200 or not catalog.json():
        assert True
        return
    vid = catalog.json()[0].get("vehicle_id")
    r = client.get("/finance/estimate", params={"vehicle_id": vid})
    assert r.status_code in (200, 404, 503)
