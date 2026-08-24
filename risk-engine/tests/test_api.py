from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_all_risks():
    response = client.get("/risk")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4

def test_get_risk_for_known_zone():
    response = client.get("/risk/Z17")
    assert response.status_code == 200
    data = response.json()
    assert data["zone_id"] == "Z17"
    assert "risk_level" in data

def test_get_risk_for_unknown_zone():
    response = client.get("/risk/Z999")
    assert response.status_code == 404

def test_calculate_custom_risk():
    payload = {
        "zone_id": "CUSTOM_01", "rainfall": 200, "river_level": 7,
        "elevation": 30, "historical_risk": 70, "drainage": 80, "trend": 20,
    }
    response = client.post("/risk/calculate", json=payload)
    assert response.status_code == 200
    assert response.json()["zone_id"] == "CUSTOM_01"

def test_zone_explanation():
    response = client.get("/zones/Z17/explanation")
    assert response.status_code == 200
    assert "explanation" in response.json()

def test_demo_scenario_valid():
    response = client.post("/demo/heavy_rain")
    assert response.status_code == 200

def test_demo_scenario_invalid():
    response = client.post("/demo/not_a_real_scenario")
    assert response.status_code == 404