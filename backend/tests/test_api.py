import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def load_payload():
    with open("../test_payload.json") as f:
        return json.load(f)

def test_health():
    r = requests.get(f"{BASE_URL}/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_predict_valid_payload():
    payload = load_payload()
    r = requests.post(f"{BASE_URL}/api/predict", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "prediction" in body
    assert body["prediction"] in ["Default", "No Default"]
    assert "risk_probability" in body
    assert "recommendations" in body

def test_predict_missing_field():
    payload = load_payload()
    del payload["dti"]
    r = requests.post(f"{BASE_URL}/api/predict", json=payload)
    assert r.status_code == 400
    assert "error" in r.json()

def test_schema_endpoint():
    r = requests.get(f"{BASE_URL}/api/schema")
    assert r.status_code == 200
    assert "raw_columns" in r.json()