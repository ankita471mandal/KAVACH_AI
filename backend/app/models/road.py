from sqlalchemy import Column, Integer, String, Float, Boolean, JSON
from .base import BaseModel

class Road(BaseModel):
    __tablename__ = "roads"
    
    name = Column(String, nullable=False)
    road_type = Column(String, default="primary")  # primary, secondary, tertiary
    
    # Status
    status = Column(String, default="OPEN")  # OPEN, BLOCKED, DAMAGED
    flood_risk = Column(Float, default=0.0)
    
    # Geometry
    geometry = Column(JSON, nullable=True)  # GeoJSON LineString
    
    # Accessibility
    accessibility_score = Column(Float, default=100.0)
    
    # Metadata
    last_updated_by = Column(String, nullable=True)
    verified = Column(Boolean, default=False)