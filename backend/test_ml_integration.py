"""
Test ML integration with Member 1's models
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_ml_hazard_prediction():
    """Test hazard prediction with ML"""
    
    hazard_data = {
        "zone_id": 1,
        "hazard_type": "flood",
        "rainfall": 150.0,
        "river_level": 8.5,
        "elevation": 45.0,
        "historical_risk": 65.0,
        "drainage_quality": 40.0,
        "forecast_trend": "increasing"
    }
    
    response = requests.post(f"{BASE_URL}/hazards/ml-predict", json=hazard_data)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ ML Hazard Prediction Test")
        print(f"   Risk Score: {result['risk_score']}")
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Using ML: {result['using_ml_model']}")
        return True
    else:
        print(f"❌ ML test failed: {response.status_code}")
        return False

def test_ml_vulnerability():
    """Test vulnerability calculation with ML"""
    
    household_data = {
        "location_lat": 28.7041,
        "location_lng": 77.1025,
        "total_population": 5,
        "children": 2,
        "elderly": 1,
        "disabled": 1,
        "medical_dependency": True,
        "building_condition": "poor"
    }
    
    response = requests.post(f"{BASE_URL}/households/", json=household_data)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ ML Vulnerability Test")
        print(f"   Vulnerability Score: {result['vulnerability_score']}")
        print(f"   Household ID: {result['id']}")
        return True
    else:
        print(f"❌ Vulnerability test failed: {response.status_code}")
        return False

if __name__ == "__main__":
    print("🧪 Testing ML Integration with Member 1\n")
    print("="*60)
    
    test_ml_hazard_prediction()
    test_ml_vulnerability()
    
    print("="*60)
    print("\n✅ ML Integration Tests Complete!")