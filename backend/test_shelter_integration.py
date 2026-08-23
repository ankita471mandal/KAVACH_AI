"""
Test shelter integration with Member 4's algorithm
"""
import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_shelter_allocation():
    """Test shelter allocation algorithm"""
    
    # Test allocation for 300 evacuees from zone 1
    response = requests.post(
        f"{BASE_URL}/shelters/allocate",
        params={
            "zone_id": 1,
            "evacuee_count": 300
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Shelter Allocation Test")
        print(f"   Total Evacuees: {result['total_evacuees']}")
        print(f"   Allocated: {result['total_allocated']}")
        print(f"   Unallocated: {result['unallocated']}")
        print(f"   Using Advanced Algorithm: {result.get('using_advanced_algorithm', False)}")
        print("\n   Allocation Details:")
        for alloc in result['allocation']:
            print(f"   - {alloc['shelter_name']}: {alloc['allocated_count']} people")
        return True
    else:
        print(f"❌ Allocation test failed: {response.status_code}")
        return False

def test_capacity_alerts():
    """Test capacity overflow alerts"""
    
    response = requests.get(f"{BASE_URL}/shelters/alerts")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Capacity Alerts Test")
        print(f"   Total Alerts: {result['total_alerts']}")
        
        if result['total_alerts'] > 0:
            print("   Alerts:")
            for alert in result['alerts']:
                print(f"   - {alert['shelter_name']}: {alert['occupancy_percent']:.1f}% ({alert['status']})")
        else:
            print("   No capacity alerts")
        
        return True
    else:
        print(f"❌ Alerts test failed: {response.status_code}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Shelter Integration with Member 4\n")
    print("="*60)
    
    test_shelter_allocation()
    test_capacity_alerts()
    
    print("="*60)
    print("\n✅ Shelter Integration Tests Complete!")