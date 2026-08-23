from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class HazardBase(BaseModel):
    """Base schema for Hazard"""
    zone_id: Optional[int] = None
    hazard_type: str = Field(default="flood", description="Type of hazard: flood, landslide, cyclone")
    rainfall: float = Field(default=0.0, ge=0, le=500, description="Rainfall in mm")
    river_level: float = Field(default=0.0, ge=0, le=20, description="River level in meters")
    elevation: Optional[float] = Field(default=None, description="Elevation in meters")
    historical_risk: float = Field(default=0.0, ge=0, le=100, description="Historical risk score")
    drainage_quality: float = Field(default=50.0, ge=0, le=100, description="Drainage quality score")
    forecast_trend: str = Field(default="stable", description="Forecast trend: increasing, stable, decreasing")
    location_lat: Optional[float] = Field(default=None, ge=-90, le=90)
    location_lng: Optional[float] = Field(default=None, ge=-180, le=180)

    @field_validator('hazard_type')
    @classmethod
    def validate_hazard_type(cls, v):
        allowed_types = ['flood', 'landslide', 'cyclone', 'earthquake']
        if v not in allowed_types:
            raise ValueError(f'Hazard type must be one of {allowed_types}')
        return v
    
    @field_validator('forecast_trend')
    @classmethod
    def validate_forecast_trend(cls, v):
        allowed_trends = ['increasing', 'stable', 'decreasing']
        if v not in allowed_trends:
            raise ValueError(f'Forecast trend must be one of {allowed_trends}')
        return v

class HazardCreate(HazardBase):
    """Schema for creating a new hazard"""
    pass

class HazardUpdate(BaseModel):
    """Schema for updating a hazard"""
    zone_id: Optional[int] = None
    rainfall: Optional[float] = Field(default=None, ge=0, le=500)
    river_level: Optional[float] = Field(default=None, ge=0, le=20)
    elevation: Optional[float] = None
    historical_risk: Optional[float] = Field(default=None, ge=0, le=100)
    drainage_quality: Optional[float] = Field(default=None, ge=0, le=100)
    forecast_trend: Optional[str] = None
    location_lat: Optional[float] = Field(default=None, ge=-90, le=90)
    location_lng: Optional[float] = Field(default=None, ge=-180, le=180)

class HazardResponse(HazardBase):
    """Schema for hazard response"""
    id: int
    risk_score: float
    risk_level: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True