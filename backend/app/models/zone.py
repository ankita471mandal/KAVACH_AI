from sqlalchemy import Column, Integer, String, Float, JSON
from .base import BaseModel

class Zone(BaseModel):
    __tablename__ = "zones"
    
    name = Column(String, nullable=False, unique=True)
    
    # Location
    center_lat = Column(Float, nullable=False)
    center_lng = Column(Float, nullable=False)
    
    # Geometry
    geometry = Column(JSON, nullable=True)  # GeoJSON Polygon
    
    # Risk
    risk_score = Column(Float, default=0.0)
    risk_level = Column(String, default="green")
    
    # Priority
    priority_score = Column(Float, default=0.0)
    priority_level = Column(String, default="P3")  # P1, P2, P3
    
    # Population
    total_population = Column(Integer, default=0)
    vulnerable_population = Column(Integer, default=0)
    
    # Infrastructure
    hospital_count = Column(Integer, default=0)
    shelter_count = Column(Integer, default=0)