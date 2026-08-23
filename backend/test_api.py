import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Test health endpoint"""
    response = requests.get("http://localhost:8000/health")
    print(f"✅ Health Check: {response.json()}")

def test_create_household():
    """Test household creation"""
    data = {
        "location_lat": 28.7041,
        "location_lng": 77.1025,
        "total_population": 5,
        "children": 2,
        "elderly": 1,
        "disabled": 0,
        "medical_dependency": True,
        "building_condition": "moderate",
        "emergency_contact": "John Doe",
        "emergency_phone": "+91-9876543210"
    }
    
    response = requests.post(f"{BASE_URL}/households/", json=data)
    print(f"✅ Household Created: {response.json()}")
    return response.json()["id"]

def test_vulnerability(household_id):
    """Test vulnerability calculation"""
    response = requests.get(f"{BASE_URL}/households/{household_id}/vulnerability")
    print(f"✅ Vulnerability: {json.dumps(response.json(), indent=2)}")

def test_sos():
    """Test SOS creation"""
    data = {
        "citizen_name": "Emergency User",
        "citizen_phone": "+91-9999999999",
        "location_lat": 28.7041,
        "location_lng": 77.1025,
        "emergency_type": "MEDICAL",
        "description": "Heart attack emergency",
        "people_count": 1
    }
    
    response = requests.post(f"{BASE_URL}/sos/", json=data)
    print(f"✅ SOS Created: {response.json()}")

def test_rescue_report():
    """Test rescue report"""
    data = {
        "reporter_name": "Rescue Team Alpha",
        "report_type": "road_blocked",
        "severity": "HIGH",
        "location_lat": 28.7041,
        "location_lng": 77.1025,
        "description": "Main road completely flooded",
        "affected_count": 0
    }
    
    response = requests.post(f"{BASE_URL}/rescue/report", json=data)
    print(f"✅ Rescue Report: {response.json()}")

if __name__ == "__main__":
    print("🧪 Starting API Tests...\n")
    
    test_health()
    household_id = test_create_household()
    test_vulnerability(household_id)
    test_sos()
    test_rescue_report()
    
    print("\n✅ All tests completed!")