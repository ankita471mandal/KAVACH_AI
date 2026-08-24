from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime

class ZoneBase(BaseModel):
    """Base schema for Zone"""
    name: str = Field(..., min_length=1, max_length=100, description="Zone identifier (e.g., Z17)")
    center_lat: float = Field(..., ge=-90, le=90, description="Center latitude")
    center_lng: float = Field(..., ge=-180, le=180, description="Center longitude")
    geometry: Optional[Dict[str, Any]] = Field(default=None, description="GeoJSON Polygon")
    total_population: int = Field(default=0, ge=0, description="Total population in zone")
    vulnerable_population: int = Field(default=0, ge=0, description="Vulnerable population count")
    hospital_count: int = Field(default=0, ge=0)
    shelter_count: int = Field(default=0, ge=0)

class ZoneCreate(ZoneBase):
    """Schema for creating a new zone"""
    pass

class ZoneUpdate(BaseModel):
    """Schema for updating a zone"""
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    center_lat: Optional[float] = Field(default=None, ge=-90, le=90)
    center_lng: Optional[float] = Field(default=None, ge=-180, le=180)
    geometry: Optional[Dict[str, Any]] = None
    total_population: Optional[int] = Field(default=None, ge=0)
    vulnerable_population: Optional[int] = Field(default=None, ge=0)
    hospital_count: Optional[int] = Field(default=None, ge=0)
    shelter_count: Optional[int] = Field(default=None, ge=0)

class ZoneResponse(ZoneBase):
    """Schema for zone response"""
    id: int
    risk_score: float
    risk_level: str
    priority_score: float
    priority_level: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True