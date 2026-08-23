from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, DateTime
from .base import BaseModel

class RescueReport(BaseModel):
    __tablename__ = "rescue_reports"
    
    # Reporter
    reporter_id = Column(Integer, nullable=True)
    reporter_name = Column(String, nullable=True)
    
    # Report details
    report_type = Column(String, nullable=False)  # road_blocked, person_trapped, etc.
    severity = Column(String, default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    
    # Location
    location_lat = Column(Float, nullable=False)
    location_lng = Column(Float, nullable=False)
    location_description = Column(String, nullable=True)
    
    # Details
    description = Column(String, nullable=True)
    affected_count = Column(Integer, default=0)
    
    # Verification
    verified = Column(Boolean, default=False)
    verified_by = Column(String, nullable=True)
    verified_at = Column(DateTime, nullable=True)
    
    # Metadata
    photo_url = Column(String, nullable=True)
    metadata = Column(JSON, nullable=True)