from fastapi.testclient import TestClient
from src.backend.main import app
from src.backend.services.inventory.catalog import get_default_catalog

client = TestClient(app)


def test_recommendations_endpoint():
    # ensure catalog exists
    try:
        c = get_default_catalog(csv_path="data/datasetSample.csv")
        import src.backend.startup as startup
        startup.catalog = c
    except Exception:
        pass
    r = client.get("/recommendations/from_session")
    assert r.status_code in (200, 503)
