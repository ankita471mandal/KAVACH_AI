from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime

class RoadBase(BaseModel):
    """Base schema for Road"""
    name: str = Field(..., min_length=1, max_length=200, description="Road name")
    road_type: str = Field(default="primary", description="Road type: primary, secondary, tertiary")
    status: str = Field(default="OPEN", description="Road status: OPEN, BLOCKED, DAMAGED, FLOODED")
    flood_risk: float = Field(default=0.0, ge=0, le=100, description="Flood risk score")
    geometry: Optional[Dict[str, Any]] = Field(default=None, description="GeoJSON LineString")
    accessibility_score: float = Field(default=100.0, ge=0, le=100, description="Accessibility score")
    last_updated_by: Optional[str] = Field(default=None, max_length=100)
    verified: bool = Field(default=False, description="Is the road status verified")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        allowed = ['OPEN', 'BLOCKED', 'DAMAGED', 'FLOODED', 'UNDER_REPAIR']
        if v not in allowed:
            raise ValueError(f'Road status must be one of {allowed}')
        return v
    
    @field_validator('road_type')
    @classmethod
    def validate_road_type(cls, v):
        allowed = ['primary', 'secondary', 'tertiary', 'residential']
        if v not in allowed:
            raise ValueError(f'Road type must be one of {allowed}')
        return v

class RoadCreate(RoadBase):
    """Schema for creating a new road"""
    pass

class RoadUpdate(BaseModel):
    """Schema for updating a road"""
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    road_type: Optional[str] = None
    status: Optional[str] = None
    flood_risk: Optional[float] = Field(default=None, ge=0, le=100)
    geometry: Optional[Dict[str, Any]] = None
    accessibility_score: Optional[float] = Field(default=None, ge=0, le=100)
    last_updated_by: Optional[str] = Field(default=None, max_length=100)
    verified: Optional[bool] = None

class RoadResponse(RoadBase):
    """Schema for road response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True