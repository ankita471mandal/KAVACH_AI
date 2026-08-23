"""
Database Initialization Script
Run this to create all tables and add sample data
"""

from sqlalchemy.orm import Session
from app.db.session import engine, SessionLocal
from app.models.base import Base
from app.models import *
import sys

def create_tables():
    """Create all database tables"""
    print("🔨 Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def add_sample_data():
    """Add sample data for testing"""
    print("\n📦 Adding sample data...")
    db = SessionLocal()
    
    try:
        # Add sample zones
        from app.models.zone import Zone
        zones = [
            Zone(
                name="Z17",
                center_lat=28.7041,
                center_lng=77.1025,
                total_population=426,
                vulnerable_population=38,
                hospital_count=1,
                shelter_count=2,
                risk_score=48.0,
                risk_level="yellow",
                priority_score=50.0,
                priority_level="P2"
            ),
            Zone(
                name="Z12",
                center_lat=28.6139,
                center_lng=77.2090,
                total_population=520,
                vulnerable_population=65,
                hospital_count=2,
                shelter_count=3,
                risk_score=35.0,
                risk_level="yellow",
                priority_score=40.0,
                priority_level="P3"
            )
        ]
        
        for zone in zones:
            db.add(zone)
        
        # Add sample hospitals
        from app.models.hospital import Hospital
        hospitals = [
            Hospital(
                name="City General Hospital",
                location_lat=28.7041,
                location_lng=77.1025,
                total_beds=200,
                available_beds=45,
                emergency_capacity_percent=78.0,
                emergency_services=True,
                ambulance_count=5,
                emergency_staff_count=20,
                road_accessibility="HIGH",
                flood_risk=15.0,
                contact_number="+91-11-1234567"
            ),
            Hospital(
                name="District Medical Center",
                location_lat=28.6139,
                location_lng=77.2090,
                total_beds=150,
                available_beds=32,
                emergency_capacity_percent=82.0,
                emergency_services=True,
                ambulance_count=3,
                emergency_staff_count=15,
                road_accessibility="HIGH",
                flood_risk=10.0,
                contact_number="+91-11-7654321"
            )
        ]
        
        for hospital in hospitals:
            db.add(hospital)
        
        # Add sample shelters
        from app.models.shelter import Shelter
        shelters = [
            Shelter(
                name="Community Shelter S1",
                location_lat=28.7100,
                location_lng=77.1100,
                total_capacity=500,
                current_occupancy=0,
                water_capacity=450,
                food_capacity=480,
                medical_capacity=100,
                sanitation_capacity=500,
                safe_capacity=450,
                available_capacity=450,
                is_operational=True,
                flood_risk=5.0,
                manager_name="Rajesh Kumar",
                contact_number="+91-98765-43210"
            ),
            Shelter(
                name="Emergency Shelter S2",
                location_lat=28.7200,
                location_lng=77.1200,
                total_capacity=800,
                current_occupancy=0,
                water_capacity=750,
                food_capacity=800,
                medical_capacity=150,
                sanitation_capacity=780,
                safe_capacity=750,
                available_capacity=750,
                is_operational=True,
                flood_risk=3.0,
                manager_name="Priya Singh",
                contact_number="+91-98765-54321"
            )
        ]
        
        for shelter in shelters:
            db.add(shelter)
        
        # Add sample roads
        from app.models.road import Road
        roads = [
            Road(
                name="Main Highway R1",
                road_type="primary",
                status="OPEN",
                flood_risk=20.0,
                accessibility_score=100.0,
                verified=True
            ),
            Road(
                name="Secondary Road R5",
                road_type="secondary",
                status="OPEN",
                flood_risk=45.0,
                accessibility_score=85.0,
                verified=True
            )
        ]
        
        for road in roads:
            db.add(road)
        
        # Add sample households
        from app.models.household import Household
        households = [
            Household(
                location_lat=28.7050,
                location_lng=77.1030,
                zone_id=1,
                total_population=5,
                children=2,
                elderly=1,
                disabled=0,
                medical_dependency=True,
                building_condition="moderate",
                vulnerability_score=75.0,
                emergency_contact="John Doe",
                emergency_phone="+91-99999-11111"
            ),
            Household(
                location_lat=28.7060,
                location_lng=77.1040,
                zone_id=1,
                total_population=4,
                children=1,
                elderly=2,
                disabled=1,
                medical_dependency=True,
                building_condition="poor",
                vulnerability_score=91.0,
                emergency_contact="Jane Smith",
                emergency_phone="+91-99999-22222"
            )
        ]
        
        for household in households:
            db.add(household)
        
        # Add sample hazard
        from app.models.hazard import Hazard
        hazards = [
            Hazard(
                zone_id=1,
                hazard_type="flood",
                rainfall=120.5,
                river_level=7.5,
                elevation=50.0,
                historical_risk=60.0,
                drainage_quality=45.0,
                forecast_trend="increasing",
                risk_score=75.0,
                risk_level="orange",
                location_lat=28.7041,
                location_lng=77.1025
            )
        ]
        
        for hazard in hazards:
            db.add(hazard)
        
        db.commit()
        print("✅ Sample data added successfully!")
        print("\n📊 Sample Data Summary:")
        print(f"   • Zones: {len(zones)}")
        print(f"   • Hospitals: {len(hospitals)}")
        print(f"   • Shelters: {len(shelters)}")
        print(f"   • Roads: {len(roads)}")
        print(f"   • Households: {len(households)}")
        print(f"   • Hazards: {len(hazards)}")
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    print("=" * 60)
    print("🚀 Kavach AI - Database Initialization")
    print("=" * 60)
    
    # Create tables
    if not create_tables():
        print("\n❌ Database initialization failed!")
        sys.exit(1)
    
    # Add sample data
    add_sample_data()
    
    print("\n" + "=" * 60)
    print("✅ Database initialization complete!")
    print("=" * 60)
    print("\n📌 Next steps:")
    print("   1. Run backend: python app/main.py")
    print("   2. Open API docs: http://localhost:8000/docs")
    print("   3. Test endpoints using the Swagger UI")

if __name__ == "__main__":
    main()