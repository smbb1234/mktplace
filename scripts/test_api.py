import requests

base = "http://localhost:8000"

def safe_json(resp):
	try:
		return resp.json()
	except Exception:
		print("REQUEST FAILED: status=", resp.status_code)
		print("BODY:\n", resp.text)
		return None

print(safe_json(requests.get(f"{base}/health")))
print((safe_json(requests.get(f"{base}/catalog")) or [])[:2])
r = requests.post(
	f"{base}/enquiries",
	json={"vehicle_id": "CAR-2026-0001", "full_name": "T Tester", "email": "t@t.com", "phone": "000"},
)
print(safe_json(r))