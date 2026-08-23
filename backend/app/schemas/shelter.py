from pydantic import BaseModel, Field, validator
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

    @validator('current_occupancy')
    def validate_occupancy(cls, v, values):
        if 'total_capacity' in values and v > values['total_capacity']:
            raise ValueError('Current occupancy cannot exceed total capacity')
        return v

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

class ShelterCapacityDetail(BaseModel):
    """Detailed shelter capacity breakdown"""
    shelter_id: int
    name: str
    location: dict = Field(default_factory=dict, description="Location coordinates")
    total_capacity: int
    current_occupancy: int
    safe_capacity: int
    available_capacity: int
    capacity_breakdown: dict = Field(default_factory=dict, description="Detailed capacity by resource")
    occupancy_percent: float
    is_accepting: bool
    flood_risk: float
    status: str
    limiting_factor: Optional[str] = Field(default=None, description="Which resource is limiting capacity")

class ShelterAllocation(BaseModel):
    """Shelter allocation recommendation"""
    shelter_id: int
    shelter_name: str
    allocated_count: int
    priority: int
    distance_km: Optional[float] = None
    route_safety_score: Optional[float] = None

class ShelterReallocationPlan(BaseModel):
    """Shelter reallocation plan for overflow"""
    required_capacity: int
    primary_shelter: Optional[ShelterAllocation] = None
    overflow_shelters: list[ShelterAllocation] = Field(default_factory=list)
    total_allocated: int
    unallocated: int
    has_deficit: bool