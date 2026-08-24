from app.schemas import (
    HazardCreate,
    HouseholdCreate,
    HospitalCreate,
    ShelterCreate,
    RoadCreate,
    RescueReportCreate,
    SOSCreate,
    ZoneCreate
)

def test_hazard_schema():
    """Test hazard schema validation"""
    hazard = HazardCreate(
        zone_id=1,
        hazard_type="flood",
        rainfall=120.5,
        river_level=7.5,
        elevation=50.0,
        historical_risk=60.0,
        drainage_quality=45.0,
        forecast_trend="increasing",
        location_lat=28.7041,
        location_lng=77.1025
    )
    print("✅ Hazard schema valid:", hazard.dict())

def test_hospital_schema():
    """Test hospital schema validation"""
    hospital = HospitalCreate(
        name="City General Hospital",
        location_lat=28.7041,
        location_lng=77.1025,
        total_beds=200,
        available_beds=45,
        emergency_services=True,
        ambulance_count=5,
        emergency_staff_count=20,
        road_accessibility="HIGH",
        flood_risk=15.5,
        contact_number="+91-9876543210"
    )
    print("✅ Hospital schema valid:", hospital.dict())

def test_shelter_schema():
    """Test shelter schema validation"""
    shelter = ShelterCreate(
        name="Community Shelter A",
        location_lat=28.7041,
        location_lng=77.1025,
        total_capacity=500,
        current_occupancy=120,
        water_capacity=450,
        food_capacity=400,
        medical_capacity=100,
        sanitation_capacity=480,
        is_operational=True,
        flood_risk=10.0
    )
    print("✅ Shelter schema valid:", shelter.dict())

def test_sos_schema():
    """Test SOS schema validation"""
    sos = SOSCreate(
        citizen_name="John Doe",
        citizen_phone="+91-9999999999",
        location_lat=28.7041,
        location_lng=77.1025,
        emergency_type="MEDICAL",
        description="Heart attack emergency",
        people_count=1
    )
    print("✅ SOS schema valid:", sos.dict())

if __name__ == "__main__":
    print("🧪 Testing Schemas...\n")
    test_hazard_schema()
    test_hospital_schema()
    test_shelter_schema()
    test_sos_schema()
    print("\n✅ All schema tests passed!")