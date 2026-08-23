"""
Shelter Service - Integration with Member 4's allocation algorithm
"""
import sys
import os

# Add shelter_algo directory to path
shelter_path = os.path.join(os.path.dirname(__file__), '../../..', 'shelter_algo')
sys.path.insert(0, shelter_path)

try:
    from allocation_algorithm import allocate_evacuees, optimize_shelter_assignment
    SHELTER_ALGO_AVAILABLE = True
except ImportError:
    print("⚠️  Shelter algorithm not found - using fallback")
    SHELTER_ALGO_AVAILABLE = False

from sqlalchemy.orm import Session
from app.models.shelter import Shelter
from app.models.zone import Zone

class ShelterService:
    """Service for shelter capacity and allocation"""
    
    @staticmethod
    def calculate_safe_capacity(shelter):
        """Calculate safe capacity based on resources"""
        return min(
            shelter.water_capacity,
            shelter.food_capacity,
            shelter.sanitation_capacity,
            shelter.medical_capacity,
            shelter.total_capacity
        )
    
    @staticmethod
    def allocate_evacuees(db: Session, zone_id: int, evacuee_count: int):
        """Allocate evacuees to shelters using Member 4's algorithm"""
        
        # Get all operational shelters
        shelters = db.query(Shelter).filter(
            Shelter.is_operational == True
        ).all()
        
        # Prepare shelter data for algorithm
        shelter_data = []
        for shelter in shelters:
            safe_capacity = ShelterService.calculate_safe_capacity(shelter)
            available = max(safe_capacity - shelter.current_occupancy, 0)
            
            shelter_data.append({
                'id': shelter.id,
                'name': shelter.name,
                'location': (shelter.location_lat, shelter.location_lng),
                'available_capacity': available,
                'flood_risk': shelter.flood_risk,
                'resources': {
                    'water': shelter.water_capacity,
                    'food': shelter.food_capacity,
                    'medical': shelter.medical_capacity
                }
            })
        
        # Use Member 4's allocation algorithm if available
        if SHELTER_ALGO_AVAILABLE:
            try:
                allocation = allocate_evacuees(
                    evacuee_count=evacuee_count,
                    shelters=shelter_data,
                    zone_id=zone_id
                )
                return allocation
            except Exception as e:
                print(f"Allocation algorithm error: {e}, using fallback")
                return ShelterService._fallback_allocation(shelter_data, evacuee_count)
        else:
            return ShelterService._fallback_allocation(shelter_data, evacuee_count)
    
    @staticmethod
    def _fallback_allocation(shelters, evacuee_count):
        """Fallback allocation if Member 4's algorithm unavailable"""
        
        # Sort by available capacity and safety
        shelters.sort(
            key=lambda x: (x['available_capacity'], -x['flood_risk']),
            reverse=True
        )
        
        allocation = []
        remaining = evacuee_count
        
        for shelter in shelters:
            if remaining <= 0:
                break
            
            allocated = min(remaining, shelter['available_capacity'])
            if allocated > 0:
                allocation.append({
                    'shelter_id': shelter['id'],
                    'shelter_name': shelter['name'],
                    'allocated_count': allocated,
                    'available_before': shelter['available_capacity'],
                    'available_after': shelter['available_capacity'] - allocated
                })
                remaining -= allocated
        
        return {
            'total_evacuees': evacuee_count,
            'total_allocated': evacuee_count - remaining,
            'unallocated': remaining,
            'allocation': allocation,
            'using_advanced_algorithm': False
        }
    
    @staticmethod
    def check_capacity_overflow(db: Session):
        """Check which shelters are approaching capacity"""
        
        shelters = db.query(Shelter).all()
        alerts = []
        
        for shelter in shelters:
            safe_capacity = ShelterService.calculate_safe_capacity(shelter)
            occupancy_percent = (shelter.current_occupancy / safe_capacity * 100) if safe_capacity > 0 else 0
            
            if occupancy_percent >= 90:
                alerts.append({
                    'shelter_id': shelter.id,
                    'shelter_name': shelter.name,
                    'occupancy_percent': occupancy_percent,
                    'available_capacity': max(safe_capacity - shelter.current_occupancy, 0),
                    'status': 'CRITICAL' if occupancy_percent >= 95 else 'WARNING'
                })
        
        return alerts