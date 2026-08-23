from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class SOSBase(BaseModel):
    """Base schema for SOS Request"""
    citizen_name: Optional[str] = Field(default=None, max_length=100)
    citizen_phone: Optional[str] = Field(default=None, max_length=20)
    location_lat: float = Field(..., ge=-90, le=90, description="Latitude")
    location_lng: float = Field(..., ge=-180, le=180, description="Longitude")
    emergency_type: str = Field(..., description="Type of emergency")
    description: Optional[str] = Field(default=None, max_length=1000)
    people_count: int = Field(default=1, ge=1, description="Number of people needing help")

    @field_validator('emergency_type')
    @classmethod
    def validate_emergency_type(cls, v):
        allowed = [
            'MEDICAL',
            'EVACUATION',
            'TRAPPED',
            'FIRE',
            'WATER_SUPPLY',
            'FOOD_SUPPLY',
            'SHELTER',
            'OTHER'
        ]
        if v not in allowed:
            raise ValueError(f'Emergency type must be one of {allowed}')
        return v
    
    @field_validator('citizen_phone')
    @classmethod
    def validate_phone(cls, v):
        if v and not v.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValueError('Phone number must contain only digits, +, -, and spaces')
        return v

class SOSCreate(SOSBase):
    """Schema for creating an SOS request"""
    pass

class SOSUpdate(BaseModel):
    """Schema for updating an SOS request"""
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is not None:
            allowed = ['PENDING', 'ASSIGNED', 'IN_PROGRESS', 'RESOLVED', 'CANCELLED']
            if v not in allowed:
                raise ValueError(f'Status must be one of {allowed}')
        return v
    
    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v):
        if v is not None:
            allowed = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
            if v not in allowed:
                raise ValueError(f'Priority must be one of {allowed}')
        return v

class SOSResponse(SOSBase):
    """Schema for SOS response"""
    id: int
    priority: str
    status: str
    assigned_to: Optional[str]
    assigned_at: Optional[datetime]
    resolved_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True