from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime

class RescueReportBase(BaseModel):
    """Base schema for Rescue Report"""
    reporter_name: Optional[str] = Field(default=None, max_length=100, description="Name of reporter")
    report_type: str = Field(..., description="Type of report")
    severity: str = Field(default="MEDIUM", description="Severity: LOW, MEDIUM, HIGH, CRITICAL")
    location_lat: float = Field(..., ge=-90, le=90, description="Latitude")
    location_lng: float = Field(..., ge=-180, le=180, description="Longitude")
    location_description: Optional[str] = Field(default=None, max_length=500)
    description: Optional[str] = Field(default=None, max_length=1000)
    affected_count: int = Field(default=0, ge=0, description="Number of people affected")
    photo_url: Optional[str] = Field(default=None, max_length=500)
    metadata: Optional[Dict[str, Any]] = Field(default=None)

    @field_validator('report_type')
    @classmethod
    def validate_report_type(cls, v):
        allowed = [
            'road_blocked', 
            'person_trapped', 
            'medical_emergency',
            'flood_depth',
            'building_damage',
            'shelter_overcrowded',
            'power_outage',
            'water_contamination'
        ]
        if v not in allowed:
            raise ValueError(f'Report type must be one of {allowed}')
        return v
    
    @field_validator('severity')
    @classmethod
    def validate_severity(cls, v):
        allowed = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        if v not in allowed:
            raise ValueError(f'Severity must be one of {allowed}')
        return v

class RescueReportCreate(RescueReportBase):
    """Schema for creating a rescue report"""
    reporter_id: Optional[int] = None

class RescueReportUpdate(BaseModel):
    """Schema for updating a rescue report"""
    report_type: Optional[str] = None
    severity: Optional[str] = None
    description: Optional[str] = Field(default=None, max_length=1000)
    affected_count: Optional[int] = Field(default=None, ge=0)
    verified: Optional[bool] = None
    verified_by: Optional[str] = Field(default=None, max_length=100)

class RescueReportResponse(RescueReportBase):
    """Schema for rescue report response"""
    id: int
    reporter_id: Optional[int]
    verified: bool
    verified_by: Optional[str]
    verified_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True