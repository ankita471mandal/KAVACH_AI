from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class ShelterBase(BaseModel):
    """Base schema for Shelter"""
    name: str = Field(..., min_length=1, max_length=200, description="Shelter name")
    location_lat: float = Field(..., ge=-90, le=90, description="Latitude")
    location_lng: float = Field(..., ge=-180, le=180, description="Longitude")
    total_capacity: int = Field(default=0, ge=0, description="Total physical capacity")
    current_occupancy: int = Field(default=0, ge=0, description="Current occupancy")
    water_capacity: int = Field(default=0, ge=0, description="Water supply capacity (persons)")
    food_capacity: int = Field(default=0, ge=0, description="Food supply capacity (persons)")
    medical_capacity: int = Field(default=0, ge=0, description="Medical support capacity (persons)")
    sanitation_capacity: int = Field(default=0, ge=0, description="Sanitation capacity (persons)")
    is_operational: bool = Field(default=True, description="Is shelter operational")
    flood_risk: float = Field(default=0.0, ge=0, le=100, description="Flood risk score")
    manager_name: Optional[str] = Field(default=None, max_length=100)
    contact_number: Optional[str] = Field(default=None, max_length=20)

class ShelterCreate(ShelterBase):
    """Schema for creating a new shelter"""
    pass

class ShelterUpdate(BaseModel):
    """Schema for updating a shelter"""
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    location_lat: Optional[float] = Field(default=None, ge=-90, le=90)
    location_lng: Optional[float] = Field(default=None, ge=-180, le=180)
    total_capacity: Optional[int] = Field(default=None, ge=0)
    current_occupancy: Optional[int] = Field(default=None, ge=0)
    water_capacity: Optional[int] = Field(default=None, ge=0)
    food_capacity: Optional[int] = Field(default=None, ge=0)
    medical_capacity: Optional[int] = Field(default=None, ge=0)
    sanitation_capacity: Optional[int] = Field(default=None, ge=0)
    is_operational: Optional[bool] = None
    flood_risk: Optional[float] = Field(default=None, ge=0, le=100)
    manager_name: Optional[str] = Field(default=None, max_length=100)
    contact_number: Optional[str] = Field(default=None, max_length=20)

class ShelterResponse(ShelterBase):
    """Schema for shelter response"""
    id: int
    safe_capacity: int
    available_capacity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True