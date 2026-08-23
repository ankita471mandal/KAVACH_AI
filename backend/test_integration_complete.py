"""
Complete Integration Test - All Members
Tests: Backend (3), ML (1), Shelter (4), Frontend (6)
"""
import requests
import json
import time

BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.CYAN}{text}{Colors.END}")
    print(f"{Colors.CYAN}{'='*70}{Colors.END}")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

# ==================== MEMBER 3 TESTS ====================

def test_backend_health():
    """Test Member 3: Backend Health"""
    print_header("Test 1: Backend Health (Member 3)")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Backend is healthy")
            print_info(f"Status: {data.get('status')}")
            print_info(f"Database: {data.get('database')}")
            return True
        else:
            print_error(f"Backend returned {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Backend not reachable: {e}")
        print_info("Start backend: cd backend && python run_server.py")
        return False

def test_backend_apis():
    """Test Member 3: All Backend APIs"""
    print_header("Test 2: Backend APIs (Member 3)")
    
    apis = {
        "Zones": "/api/v1/zones/",
        "Hospitals": "/api/v1/hospitals/",
        "Shelters": "/api/v1/shelters/",
        "Households": "/api/v1/households/",
        "Roads": "/api/v1/roads/",
    }
    
    all_passed = True
    for name, endpoint in apis.items():
        try:
            response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print_success(f"{name}: {len(data)} items")
            else:
                print_error(f"{name} failed: {response.status_code}")
                all_passed = False
        except Exception as e:
            print_error(f"{name} error: {e}")
            all_passed = False
    
    return all_passed

# ==================== MEMBER 1 TESTS ====================

def test_ml_risk_calculation():
    """Test Member 1: ML Risk Calculation"""
    print_header("Test 3: ML Risk Calculation (Member 1)")
    
    try:
        # Create hazard with risk calculation
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
        
        response = requests.post(
            f"{BACKEND_URL}/api/v1/hazards/",
            json=hazard_data,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print_success("Hazard created with ML risk calculation")
            print_info(f"Hazard ID: {result['id']}")
            print_info(f"Risk Score: {result['risk_score']:.2f}")
            print_info(f"Risk Level: {result['risk_level']}")
            return True
        else:
            print_error(f"Hazard creation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"ML integration error: {e}")
        return False

def test_vulnerability_scoring():
    """Test Member 1: Vulnerability Scoring"""
    print_header("Test 4: Vulnerability Scoring (Member 1)")
    
    try:
        # Get households
        response = requests.get(f"{BACKEND_URL}/api/v1/households/", timeout=5)
        
        if response.status_code == 200:
            households = response.json()
            if households:
                # Check vulnerability for first household
                hh_id = households[0]['id']
                vuln_response = requests.get(
                    f"{BACKEND_URL}/api/v1/households/{hh_id}/vulnerability",
                    timeout=5
                )
                
                if vuln_response.status_code == 200:
                    vuln_data = vuln_response.json()
                    print_success("Vulnerability calculation working")
                    print_info(f"Household ID: {vuln_data['household_id']}")
                    print_info(f"Vulnerability Score: {vuln_data['vulnerability_score']}")
                    print_info(f"Reasons: {', '.join(vuln_data['reasons'])}")
                    return True
            
            print_error("No households found for testing")
            return False
        else:
            print_error(f"Failed to get households: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Vulnerability test error: {e}")
        return False

# ==================== MEMBER 4 TESTS ====================

def test_shelter_capacity():
    """Test Member 4: Shelter Capacity Management"""
    print_header("Test 5: Shelter Capacity (Member 4)")
    
    try:
        # Get all shelters
        response = requests.get(f"{BACKEND_URL}/api/v1/shelters/", timeout=5)
        
        if response.status_code == 200:
            shelters = response.json()
            print_success(f"Found {len(shelters)} shelters")
            
            for shelter in shelters[:2]:  # Show first 2
                print_info(f"📍 {shelter['name']}")
                print(f"   Total Capacity: {shelter['total_capacity']}")
                print(f"   Available: {shelter['available_capacity']}")
                print(f"   Safe Capacity: {shelter['safe_capacity']}")
            
            return True
        else:
            print_error(f"Shelter API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Shelter test error: {e}")
        return False

def test_shelter_allocation_logic():
    """Test Member 4: Shelter Allocation Algorithm"""
    print_header("Test 6: Shelter Allocation Logic (Member 4)")
    
    try:
        # Get shelters
        shelters_response = requests.get(f"{BACKEND_URL}/api/v1/shelters/", timeout=5)
        
        if shelters_response.status_code == 200:
            shelters = shelters_response.json()
            
            # Simulate allocation
            evacuees = 300
            allocated = 0
            allocation_plan = []
            
            # Sort by available capacity
            sorted_shelters = sorted(
                shelters,
                key=lambda x: x['available_capacity'],
                reverse=True
            )
            
            for shelter in sorted_shelters:
                if evacuees <= 0:
                    break
                
                can_allocate = min(evacuees, shelter['available_capacity'])
                if can_allocate > 0:
                    allocated += can_allocate
                    evacuees -= can_allocate
                    allocation_plan.append({
                        'shelter': shelter['name'],
                        'allocated': can_allocate
                    })
            
            print_success(f"Allocation simulation complete")
            print_info(f"Total to evacuate: 300")
            print_info(f"Successfully allocated: {allocated}")
            print_info(f"Remaining: {300 - allocated}")
            
            for plan in allocation_plan:
                print(f"   → {plan['shelter']}: {plan['allocated']} people")
            
            return True
        else:
            print_error("Failed to get shelter data")
            return False
            
    except Exception as e:
        print_error(f"Allocation test error: {e}")
        return False

# ==================== MEMBER 6 TESTS ====================

def test_frontend_connection():
    """Test Member 6: Frontend Connection"""
    print_header("Test 7: Frontend Connection (Member 6)")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print_success("Frontend is accessible")
            print_info(f"URL: {FRONTEND_URL}")
            return True
        else:
            print_error(f"Frontend returned {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Frontend not reachable: {e}")
        print_info("Start frontend: cd frontend && npm start")
        return False

def test_sos_functionality():
    """Test Member 6: SOS Emergency Functionality"""
    print_header("Test 8: SOS Emergency System (Member 6)")
    
    try:
        # Create SOS request
        sos_data = {
            "citizen_name": "Integration Test User",
            "citizen_phone": "+91-9999999999",
            "location_lat": 28.7041,
            "location_lng": 77.1025,
            "emergency_type": "MEDICAL",
            "description": "Integration test emergency",
            "people_count": 1
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/v1/sos/",
            json=sos_data,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print_success("SOS system working")
            print_info(f"SOS ID: {result['id']}")
            print_info(f"Priority: {result['priority']}")
            print_info(f"Status: {result['status']}")
            return True
        else:
            print_error(f"SOS creation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"SOS test error: {e}")
        return False

# ==================== INTEGRATION TESTS ====================

def test_complete_workflow():
    """Test Complete Disaster Response Workflow"""
    print_header("Test 9: Complete Disaster Response Workflow")
    
    try:
        print_info("Step 1: Create hazard event...")
        hazard_data = {
            "zone_id": 1,
            "hazard_type": "flood",
            "rainfall": 180.0,
            "river_level": 9.0,
            "forecast_trend": "increasing"
        }
        hazard_response = requests.post(
            f"{BACKEND_URL}/api/v1/hazards/",
            json=hazard_data,
            timeout=5
        )
        
        if hazard_response.status_code != 200:
            print_error("Failed to create hazard")
            return False
        
        hazard = hazard_response.json()
        print_success(f"Hazard created (Risk: {hazard['risk_level']})")
        
        print_info("Step 2: Get priority zones...")
        priority_response = requests.get(
            f"{BACKEND_URL}/api/v1/zones/priority/list",
            timeout=5
        )
        
        if priority_response.status_code != 200:
            print_error("Failed to get priority zones")
            return False
        
        priority_data = priority_response.json()
        print_success(f"Found {len(priority_data['priority_zones'])} priority zones")
        
        print_info("Step 3: Check shelter availability...")
        shelters_response = requests.get(
            f"{BACKEND_URL}/api/v1/shelters/",
            timeout=5
        )
        
        if shelters_response.status_code != 200:
            print_error("Failed to get shelters")
            return False
        
        shelters = shelters_response.json()
        total_capacity = sum(s['available_capacity'] for s in shelters)
        print_success(f"Total shelter capacity: {total_capacity}")
        
        print_info("Step 4: Submit rescue report...")
        report_data = {
            "reporter_name": "Integration Test Team",
            "report_type": "road_blocked",
            "severity": "HIGH",
            "location_lat": 28.7041,
            "location_lng": 77.1025,
            "description": "Test road blockage"
        }
        report_response = requests.post(
            f"{BACKEND_URL}/api/v1/rescue/report",
            json=report_data,
            timeout=5
        )
        
        if report_response.status_code != 200:
            print_error("Failed to submit rescue report")
            return False
        
        print_success("Rescue report submitted")
        
        print_success("✨ Complete workflow test PASSED!")
        return True
        
    except Exception as e:
        print_error(f"Workflow error: {e}")
        return False

# ==================== MAIN TEST RUNNER ====================

def main():
    print(f"\n{Colors.CYAN}{'#'*70}{Colors.END}")
    print(f"{Colors.CYAN}# KAVACH AI - COMPLETE INTEGRATION TEST SUITE{Colors.END}")
    print(f"{Colors.CYAN}# Testing Members: 1 (AI/ML), 3 (Backend), 4 (Shelter), 6 (Frontend){Colors.END}")
    print(f"{Colors.CYAN}{'#'*70}{Colors.END}")
    
    # Wait for services to be ready
    print_info("Waiting for services to start...")
    time.sleep(2)
    
    results = {}
    
    # Run all tests
    tests = [
        ("Backend Health", test_backend_health),
        ("Backend APIs", test_backend_apis),
        ("ML Risk Calculation", test_ml_risk_calculation),
        ("Vulnerability Scoring", test_vulnerability_scoring),
        ("Shelter Capacity", test_shelter_capacity),
        ("Shelter Allocation", test_shelter_allocation_logic),
        ("Frontend Connection", test_frontend_connection),
        ("SOS System", test_sos_functionality),
        ("Complete Workflow", test_complete_workflow),
    ]
    
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print_error(f"Test '{name}' crashed: {e}")
            results[name] = False
    
    # Print summary
    print_header("TEST SUMMARY")
    
    for name, passed in results.items():
        status = f"{Colors.GREEN}✅ PASSED{Colors.END}" if passed else f"{Colors.RED}❌ FAILED{Colors.END}"
        print(f"{name}: {status}")
    
    print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
    total = len(results)
    passed = sum(results.values())
    print(f"Total Tests: {total}")
    print(f"Passed: {Colors.GREEN}{passed}{Colors.END}")
    print(f"Failed: {Colors.RED}{total - passed}{Colors.END}")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    print(f"{Colors.CYAN}{'='*70}{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}🎉 All integration tests PASSED!{Colors.END}")
        print(f"{Colors.GREEN}All members' work is successfully integrated!{Colors.END}")
    else:
        print(f"\n{Colors.YELLOW}⚠️  Some tests failed. Please check above for details.{Colors.END}")
        print(f"\n{Colors.BLUE}Troubleshooting:{Colors.END}")
        print(f"- Start backend: cd backend && python run_server.py")
        print(f"- Start frontend: cd frontend && npm start")

if __name__ == "__main__":
    main()