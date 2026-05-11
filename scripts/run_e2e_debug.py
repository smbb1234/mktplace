import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from src.backend.main import app
from src.backend.services.inventory.catalog import get_default_catalog

client = TestClient(app)

def run():
    print('GET /health')
    r = client.get('/health')
    print(r.status_code, r.text)

    print('\nPOST /chat/message')
    r = client.post('/chat/message', json={'message': "I'm looking to buy, budget £300 per month"})
    print(r.status_code, r.text)

    print('\nGET /recommendations/from_session')
    r = client.get('/recommendations/from_session')
    print(r.status_code, r.text)
    if r.status_code == 503:
        print('Attempting to load sample catalog')
        try:
            c = get_default_catalog(csv_path='data/datasetSample.csv')
            import src.backend.startup as startup
            startup.catalog = c
            print('Catalog loaded, retrying')
            r = client.get('/recommendations/from_session')
            print(r.status_code, r.text)
        except Exception as e:
            print('Failed to load catalog:', e)

    print('\nGET /catalog/')
    r = client.get('/catalog/')
    print(r.status_code)
    print(r.text[:1000])

    if r.status_code == 200 and r.json():
        vid = r.json()[0].get('vehicle_id')
        enquiry = {
            'vehicle_id': vid,
            'full_name': 'E2E Debug',
            'email': 'e2e.debug@example.com',
            'phone': '+447700900011'
        }
        print('\nPOST /enquiries/')
        er = client.post('/enquiries/', json=enquiry)
        print(er.status_code, er.text)

if __name__ == '__main__':
    run()
