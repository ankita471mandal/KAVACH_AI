from sqlalchemy import Column, Integer, String, Float, DateTime
from .base import BaseModel

class Hazard(BaseModel):
    __tablename__ = "hazards"
    
    zone_id = Column(Integer, nullable=True)
    
    # Hazard type
    hazard_type = Column(String, default="flood")  # flood, landslide, cyclone
    
    # Weather data
    rainfall = Column(Float, default=0.0)
    river_level = Column(Float, default=0.0)
    
    # Risk calculation
    elevation = Column(Float, nullable=True)
    historical_risk = Column(Float, default=0.0)
    drainage_quality = Column(Float, default=50.0)
    forecast_trend = Column(String, default="stable")  # increasing, stable, decreasing
    
    # Risk score
    risk_score = Column(Float, default=0.0)
    risk_level = Column(String, default="green")  # green, yellow, orange, red
    
    # Location
    location_lat = Column(Float, nullable=True)
    location_lng = Column(Float, nullable=True)