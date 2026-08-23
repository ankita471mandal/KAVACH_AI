from sqlalchemy import Column, Integer, String, Float, DateTime
from .base import BaseModel

class SOSRequest(BaseModel):
    __tablename__ = "sos_requests"
    
    # Requester
    citizen_name = Column(String, nullable=True)
    citizen_phone = Column(String, nullable=True)
    
    # Location
    location_lat = Column(Float, nullable=False)
    location_lng = Column(Float, nullable=False)
    
    # Emergency type
    emergency_type = Column(String, nullable=False)  # MEDICAL, EVACUATION, TRAPPED
    priority = Column(String, default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    
    # Status
    status = Column(String, default="PENDING")  # PENDING, ASSIGNED, IN_PROGRESS, RESOLVED
    
    # Assignment
    assigned_to = Column(String, nullable=True)
    assigned_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    
    # Details
    description = Column(String, nullable=True)
    people_count = Column(Integer, default=1)