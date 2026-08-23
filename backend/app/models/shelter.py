from sqlalchemy import Column, Integer, String, Float, Boolean
from .base import BaseModel

class Shelter(BaseModel):
    __tablename__ = "shelters"
    
    name = Column(String, nullable=False)
    location_lat = Column(Float, nullable=False)
    location_lng = Column(Float, nullable=False)
    
    # Capacity
    total_capacity = Column(Integer, default=0)
    current_occupancy = Column(Integer, default=0)
    available_capacity = Column(Integer, default=0)
    
    # Resources
    water_capacity = Column(Integer, default=0)
    food_capacity = Column(Integer, default=0)
    medical_capacity = Column(Integer, default=0)
    sanitation_capacity = Column(Integer, default=0)
    
    # Safe capacity (minimum of all resources)
    safe_capacity = Column(Integer, default=0)
    
    # Status
    is_operational = Column(Boolean, default=True)
    flood_risk = Column(Float, default=0.0)
    
    # Contact
    manager_name = Column(String, nullable=True)
    contact_number = Column(String, nullable=True)