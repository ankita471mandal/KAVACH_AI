from sqlalchemy import Column, Integer, String, Float, Boolean, JSON
from .base import BaseModel

class Household(BaseModel):
    __tablename__ = "households"
    
    location_lat = Column(Float, nullable=False)
    location_lng = Column(Float, nullable=False)
    zone_id = Column(Integer, nullable=True)
    
    # Population details
    total_population = Column(Integer, default=0)
    children = Column(Integer, default=0)
    elderly = Column(Integer, default=0)
    disabled = Column(Integer, default=0)
    
    # Medical needs
    medical_dependency = Column(Boolean, default=False)
    medical_details = Column(String, nullable=True)
    
    # Building condition
    building_condition = Column(String, default="good")  # good, moderate, poor
    
    # Vulnerability score
    vulnerability_score = Column(Float, default=0.0)
    
    # Emergency contact
    emergency_contact = Column(String, nullable=True)
    emergency_phone = Column(String, nullable=True)
    
    # Additional data
    metadata = Column(JSON, nullable=True)