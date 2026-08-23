import requests
import time

def verify_all():
    print("="*60)
    print("🔍 Kavach AI - Complete Verification")
    print("="*60)
    
    # Test Backend
    print("\n1. Testing Backend...")
    try:
        health = requests.get("http://localhost:8000/health", timeout=5)
        if health.status_code == 200:
            print("   ✅ Backend is healthy")
        else:
            print(f"   ❌ Backend returned status {health.status_code}")
            return False
    except:
        print("   ❌ Backend not reachable")
        print("   ℹ️  Start it with: cd backend && python run_server.py")
        return False
    
    # Test Frontend
    print("\n2. Testing Frontend...")
    try:
        frontend = requests.get("http://localhost:3000", timeout=5)
        if frontend.status_code == 200:
            print("   ✅ Frontend is accessible")
        else:
            print(f"   ❌ Frontend returned status {frontend.status_code}")
    except:
        print("   ❌ Frontend not reachable")
        print("   ℹ️  Start it with: cd frontend && npm start")
        return False
    
    # Test APIs
    print("\n3. Testing APIs...")
    endpoints = {
        "Zones": "/api/v1/zones/",
        "Hospitals": "/api/v1/hospitals/",
        "Shelters": "/api/v1/shelters/",
    }
    
    for name, endpoint in endpoints.items():
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {name}: {len(data)} items")
            else:
                print(f"   ❌ {name} failed")
        except Exception as e:
            print(f"   ❌ {name} error: {e}")
    
    print("\n" + "="*60)
    print("✅ Verification Complete!")
    print("="*60)
    print("\n📌 Access Points:")
    print("   Backend API:  http://localhost:8000/docs")
    print("   Frontend App: http://localhost:3000")
    
    return True

if __name__ == "__main__":
    time.sleep(2)  # Wait for services to start
    verify_all()