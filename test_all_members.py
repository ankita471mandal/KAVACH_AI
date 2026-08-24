"""
Complete Integration Test - All 4 Members
Member 1: AI/ML
Member 3: Backend
Member 4: Shelter
Member 6: Frontend
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"

def test_all_members():
    print("="*70)
    print("🧪 KAVACH AI - ALL MEMBERS INTEGRATION TEST")
    print("="*70)
    
    time.sleep(2)
    
    # Test Member 3: Backend
    print("\n✅ Testing Member 3 (Backend)...")
    health = requests.get(f"{BASE_URL}/health")
    assert health.status_code == 200
    print(f"   Backend: {health.json()['status']}")
    
    # Test Member 1: ML Risk
    print("\n✅ Testing Member 1 (AI/ML)...")
    hazard = requests.post(f"{BASE_URL}/api/v1/hazards/", json={
        "zone_id": 1,
        "hazard_type": "flood",
        "rainfall": 180.0,
        "river_level": 9.0,
        "forecast_trend": "increasing"
    })
    assert hazard.status_code == 200
    print(f"   Risk Score: {hazard.json()['risk_score']}")
    print(f"   Risk Level: {hazard.json()['risk_level']}")
    
    # Test Member 4: Shelter
    print("\n✅ Testing Member 4 (Shelter)...")
    shelters = requests.get(f"{BASE_URL}/api/v1/shelters/")
    assert shelters.status_code == 200
    total_capacity = sum(s['available_capacity'] for s in shelters.json())
    print(f"   Total Shelter Capacity: {total_capacity}")
    
    # Test Member 6: SOS
    print("\n✅ Testing Member 6 (Frontend/SOS)...")
    sos = requests.post(f"{BASE_URL}/api/v1/sos/", json={
        "citizen_name": "Test User",
        "location_lat": 28.7041,
        "location_lng": 77.1025,
        "emergency_type": "MEDICAL",
        "description": "Integration test"
    })
    assert sos.status_code == 200
    print(f"   SOS ID: {sos.json()['id']}")
    print(f"   Priority: {sos.json()['priority']}")
    
    print("\n" + "="*70)
    print("🎉 ALL MEMBERS INTEGRATED SUCCESSFULLY!")
    print("="*70)

if __name__ == "__main__":
    try:
        test_all_members()
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        print("\nMake sure:")
        print("  1. Backend is running: python run_server.py")
        print("  2. Database is initialized: python run_init_db.py")