from pydantic import BaseModel, Field, validator
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

    @validator('vulnerable_population')
    def validate_vulnerable_population(cls, v, values):
        if 'total_population' in values and v > values['total_population']:
            raise ValueError('Vulnerable population cannot exceed total population')
        return v

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

class ZonePriorityDetail(BaseModel):
    """Detailed zone priority information"""
    zone_id: int
    zone_name: str
    priority_score: float
    priority_level: str
    risk_score: float
    risk_level: str
    reasons: list[str] = Field(default_factory=list)
    recommended_action: str
    total_population: int
    vulnerable_population: int
    shelter_capacity_status: str
    hospital_accessibility: str
    evacuation_required: bool
    estimated_evacuees: int

class ZoneRiskFactors(BaseModel):
    """Zone risk factor breakdown"""
    zone_id: int
    zone_name: str
    flood_exposure: float
    vulnerable_households: int
    hospital_accessibility_score: float
    main_road_status: str
    shelter_capacity_ratio: float
    risk_trend: str
    overall_risk: float

class ZonePriorityList(BaseModel):
    """List of priority zones"""
    priority_zones: list[ZonePriorityDetail] = Field(default_factory=list)
    total_zones: int
    critical_zones: int
    high_priority_zones: int
    total_affected_population: int
    last_updated: datetime