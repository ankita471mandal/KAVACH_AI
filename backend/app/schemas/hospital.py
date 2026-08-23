from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class HospitalBase(BaseModel):
    """Base schema for Hospital"""
    name: str = Field(..., min_length=1, max_length=200, description="Hospital name")
    location_lat: float = Field(..., ge=-90, le=90, description="Latitude")
    location_lng: float = Field(..., ge=-180, le=180, description="Longitude")
    total_beds: int = Field(default=0, ge=0, description="Total bed capacity")
    available_beds: int = Field(default=0, ge=0, description="Currently available beds")
    emergency_services: bool = Field(default=True, description="Has emergency services")
    ambulance_count: int = Field(default=0, ge=0, description="Number of ambulances")
    emergency_staff_count: int = Field(default=0, ge=0, description="Emergency staff count")
    road_accessibility: str = Field(default="HIGH", description="Road accessibility: HIGH, MEDIUM, LOW")
    flood_risk: float = Field(default=0.0, ge=0, le=100, description="Flood risk score")
    contact_number: Optional[str] = Field(default=None, max_length=20)

    @field_validator('road_accessibility')
    @classmethod
    def validate_accessibility(cls, v):
        allowed = ['HIGH', 'MEDIUM', 'LOW', 'BLOCKED']
        if v not in allowed:
            raise ValueError(f'Road accessibility must be one of {allowed}')
        return v

class HospitalCreate(HospitalBase):
    """Schema for creating a new hospital"""
    pass

class HospitalUpdate(BaseModel):
    """Schema for updating a hospital"""
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    location_lat: Optional[float] = Field(default=None, ge=-90, le=90)
    location_lng: Optional[float] = Field(default=None, ge=-180, le=180)
    total_beds: Optional[int] = Field(default=None, ge=0)
    available_beds: Optional[int] = Field(default=None, ge=0)
    emergency_services: Optional[bool] = None
    ambulance_count: Optional[int] = Field(default=None, ge=0)
    emergency_staff_count: Optional[int] = Field(default=None, ge=0)
    road_accessibility: Optional[str] = None
    flood_risk: Optional[float] = Field(default=None, ge=0, le=100)
    contact_number: Optional[str] = Field(default=None, max_length=20)

class HospitalResponse(HospitalBase):
    """Schema for hospital response"""
    id: int
    emergency_capacity_percent: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True