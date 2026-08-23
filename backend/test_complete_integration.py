"""
Complete Integration Test for Kavach AI
Tests all 4 members' components working together
"""
import requests
import time
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"
API_V1 = f"{BACKEND_URL}/api/v1"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_section(title):
    print(f"\n{'='*70}")
    print(f"{Colors.BLUE}{title}{Colors.END}")
    print('='*70)

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.YELLOW}ℹ️  {msg}{Colors.END}")

# Test 1: Backend Health
def test_backend_health():
    print_section("Test 1: Backend Health (Member 3)")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Backend is healthy: {data}")
            return True
        else:
            print_error(f"Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Backend not reachable: {e}")
        print_info("Make sure backend is running: python run_server.py")
        return False

# Test 2: ML Integration (Member 1)
def test_ml_integration():
    print_section("Test 2: ML/AI Integration (Member 1)")
    try:
        # Test hazard prediction
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
        
        response = requests.post(f"{API_V1}/hazards/ml-predict", json=hazard_data)
        
        if response.status_code == 200:
            result = response.json()
            print_success(f"ML Risk Prediction: {result['risk_score']:.2f}")
            print_info(f"Risk Level: {result['risk_level']}")
            print_info(f"Using ML Model: {result.get('using_ml_model', False)}")
            return True
        else:
            print_error("ML prediction failed")
            return False
    except Exception as e:
        print_error(f"ML integration error: {e}")
        return False

# Test 3: Shelter Allocation (Member 4)
def test_shelter_allocation():
    print_section("Test 3: Shelter Allocation (Member 4)")
    try:
        # Test allocation
        response = requests.post(
            f"{API_V1}/shelters/allocate",
            params={"zone_id": 1, "evacuee_count": 300}
        )
        
        if response.status_code == 200:
            result = response.json()
            print_success(f"Allocation Complete:")
            print_info(f"  Total Evacuees: {result['total_evacuees']}")
            print_info(f"  Allocated: {result['total_allocated']}")
            print_info(f"  Unallocated: {result['unallocated']}")
            
            for alloc in result['allocation']:
                print(f"    - {alloc['shelter_name']}: {alloc['allocated_count']} people")
            
            return True
        else:
            print_error("Shelter allocation failed")
            return False
    except Exception as e:
        print_error(f"Shelter allocation error: {e}")
        return False

# Test 4: Frontend Connectivity (Member 6)
def test_frontend():
    print_section("Test 4: Frontend Dashboard (Member 6)")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print_success("Frontend is accessible")
            print_info(f"Dashboard URL: {FRONTEND_URL}")
            return True
        else:
            print_error(f"Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Frontend not reachable: {e}")
        print_info("Make sure frontend is running: npm start")
        return False

# Test 5: Complete Workflow
def test_complete_workflow():
    print_section("Test 5: Complete Disaster Response Workflow")
    
    try:
        # Step 1: Create hazard (Member 1 + Member 3)
        print_info("Step 1: Creating hazard event...")
        hazard = requests.post(f"{API_V1}/hazards/", json={
            "zone_id": 1,
            "hazard_type": "flood",
            "rainfall": 180.0,
            "river_level": 9.5,
            "elevation": 40.0,
            "historical_risk": 70.0,
            "drainage_quality": 35.0,
            "forecast_trend": "increasing"
        })
        
        if hazard.status_code == 200:
            hazard_data = hazard.json()
            print_success(f"Hazard created: Risk Score = {hazard_data['risk_score']:.2f}")
        else:
            print_error("Failed to create hazard")
            return False
        
        # Step 2: Get priority zones (Member 3)
        print_info("Step 2: Identifying priority zones...")
        priority = requests.get(f"{API_V1}/zones/priority/list")
        
        if priority.status_code == 200:
            priority_data = priority.json()
            print_success(f"Found {len(priority_data['priority_zones'])} priority zones")
            for zone in priority_data['priority_zones'][:3]:
                print(f"    - {zone['zone_name']}: Priority {zone['priority_score']:.1f}")
        else:
            print_error("Failed to get priority zones")
            return False
        
        # Step 3: Allocate shelters (Member 4 + Member 3)
        print_info("Step 3: Allocating evacuees to shelters...")
        allocation = requests.post(
            f"{API_V1}/shelters/allocate",
            params={"zone_id": 1, "evacuee_count": 426}
        )
        
        if allocation.status_code == 200:
            alloc_data = allocation.json()
            print_success(f"Allocated {alloc_data['total_allocated']} / {alloc_data['total_evacuees']} evacuees")
        else:
            print_error("Failed to allocate shelters")
            return False
        
        # Step 4: Create SOS (Member 6 + Member 3)
        print_info("Step 4: Creating SOS request...")
        sos = requests.post(f"{API_V1}/sos/", json={
            "citizen_name": "Integration Test User",
            "citizen_phone": "+91-9999999999",
            "location_lat": 28.7041,
            "location_lng": 77.1025,
            "emergency_type": "MEDICAL",
            "description": "Test medical emergency",
            "people_count": 1
        })
        
        if sos.status_code == 200:
            sos_data = sos.json()
            print_success(f"SOS created: Priority = {sos_data['priority']}")
        else:
            print_error("Failed to create SOS")
            return False
        
        # Step 5: Submit rescue report (Member 6 + Member 3)
        print_info("Step 5: Submitting rescue team report...")
        report = requests.post(f"{API_V1}/rescue/report", json={
            "reporter_name": "Integration Test Team",
            "report_type": "road_blocked",
            "severity": "HIGH",
            "location_lat": 28.7041,
            "location_lng": 77.1025,
            "description": "Test road blockage report"
        })
        
        if report.status_code == 200:
            print_success("Rescue report submitted")
        else:
            print_error("Failed to submit rescue report")
            return False
        
        print_success("🎉 Complete workflow executed successfully!")
        return True
        
    except Exception as e:
        print_error(f"Workflow error: {e}")
        return False

# Test 6: Data Consistency
def test_data_consistency():
    print_section("Test 6: Data Consistency Check")
    
    try:
        # Get zones
        zones_response = requests.get(f"{API_V1}/zones/")
        zones = zones_response.json()
        print_info(f"Total Zones: {len(zones)}")
        
        # Get hospitals
        hospitals_response = requests.get(f"{API_V1}/hospitals/")
        hospitals = hospitals_response.json()
        print_info(f"Total Hospitals: {len(hospitals)}")
        
        # Get shelters
        shelters_response = requests.get(f"{API_V1}/shelters/")
        shelters = shelters_response.json()
        print_info(f"Total Shelters: {len(shelters)}")
        
        # Get households
        households_response = requests.get(f"{API_V1}/households/")
        households = households_response.json()
        print_info(f"Total Households: {len(households)}")
        
        # Verify data exists
        if len(zones) > 0 and len(hospitals) > 0 and len(shelters) > 0:
            print_success("Database populated with sample data")
            return True
        else:
            print_error("Database is missing data")
            print_info("Run: python run_init_db.py")
            return False
        
    except Exception as e:
        print_error(f"Data consistency check failed: {e}")
        return False

# Main Test Runner
def run_all_tests():
    print(f"\n{'#'*70}")
    print(f"# {Colors.GREEN}KAVACH AI - COMPLETE INTEGRATION TEST SUITE{Colors.END}")
    print(f"# Testing Members: 1 (AI/ML), 3 (Backend), 4 (Shelter), 6 (Frontend)")
    print(f"# Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*70}\n")
    
    results = {}
    
    # Run all tests
    results['Backend Health'] = test_backend_health()
    time.sleep(1)
    
    results['ML Integration'] = test_ml_integration()
    time.sleep(1)
    
    results['Shelter Allocation'] = test_shelter_allocation()
    time.sleep(1)
    
    results['Frontend Dashboard'] = test_frontend()
    time.sleep(1)
    
    results['Data Consistency'] = test_data_consistency()
    time.sleep(1)
    
    results['Complete Workflow'] = test_complete_workflow()
    
    # Summary
    print_section("TEST SUMMARY")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    for test_name, result in results.items():
        status = f"{Colors.GREEN}✅ PASSED{Colors.END}" if result else f"{Colors.RED}❌ FAILED{Colors.END}"
        print(f"{test_name}: {status}")
    
    print(f"\n{'='*70}")
    print(f"Total Tests: {total}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.END}")
    print(f"{Colors.RED}Failed: {failed}{Colors.END}")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    print(f"{'='*70}\n")
    
    if passed == total:
        print(f"{Colors.GREEN}🎉 ALL TESTS PASSED! Integration is successful!{Colors.END}")
        print(f"\n{Colors.BLUE}Next Steps:{Colors.END}")
        print("1. Access Dashboard: http://localhost:3000")
        print("2. API Documentation: http://localhost:8000/docs")
        print("3. Prepare demo scenario")
        print("4. Ready for presentation! 🚀")
    else:
        print(f"{Colors.YELLOW}⚠️  Some tests failed. Please check above for details.{Colors.END}")
        print(f"\n{Colors.BLUE}Troubleshooting:{Colors.END}")
        if not results['Backend Health']:
            print("- Start backend: cd backend && python run_server.py")
        if not results['Frontend Dashboard']:
            print("- Start frontend: cd frontend && npm start")
        if not results['Data Consistency']:
            print("- Initialize database: cd backend && python run_init_db.py")

if __name__ == "__main__":
    run_all_tests()