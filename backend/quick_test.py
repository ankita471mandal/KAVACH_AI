"""
Quick API Test
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Quick API Test\n")
    
    tests = {
        "Health Check": f"{BASE_URL}/health",
        "Stats": f"{BASE_URL}/stats",
        "Zones": f"{BASE_URL}/api/v1/zones/",
        "Hospitals": f"{BASE_URL}/api/v1/hospitals/",
        "Shelters": f"{BASE_URL}/api/v1/shelters/",
        "Households": f"{BASE_URL}/api/v1/households/",
    }
    
    for name, url in tests.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"✅ {name}: OK")
            else:
                print(f"❌ {name}: Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
    
    print("\n✅ Quick test complete!")

if __name__ == "__main__":
    test_api()