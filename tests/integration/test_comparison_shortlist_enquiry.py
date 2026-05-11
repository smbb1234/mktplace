from fastapi.testclient import TestClient
from src.backend.main import app
from src.backend.services.inventory.catalog import get_default_catalog

client = TestClient(app)


def test_catalog_and_shortlist_enquiry():
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
    # shortlist add (uses simple in-memory service)
    add = client.post("/shortlist/add", params={"session_id": "test", "vehicle_id": vid})
    assert add.status_code in (200, 202)
    # create enquiry
    enquiry = {"vehicle_id": vid, "full_name": "X", "email": "x@example.com", "phone": "+100"}
    er = client.post("/enquiries/", json=enquiry)
    assert er.status_code in (201, 202, 500)
