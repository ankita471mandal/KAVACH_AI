from sqlalchemy import Column, Integer, String, Float, Boolean
from .base import BaseModel

class Hospital(BaseModel):
    __tablename__ = "hospitals"
    
    name = Column(String, nullable=False)
    location_lat = Column(Float, nullable=False)
    location_lng = Column(Float, nullable=False)
    
    # Capacity
    total_beds = Column(Integer, default=0)
    available_beds = Column(Integer, default=0)
    emergency_capacity_percent = Column(Float, default=0.0)
    
    # Services
    emergency_services = Column(Boolean, default=True)
    ambulance_count = Column(Integer, default=0)
    emergency_staff_count = Column(Integer, default=0)
    
    # Accessibility
    road_accessibility = Column(String, default="HIGH")  # HIGH, MEDIUM, LOW
    flood_risk = Column(Float, default=0.0)
    
    # Contact
    contact_number = Column(String, nullable=True)