from pydantic import BaseModel, Field, validator
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

    @validator('hazard_type')
    def validate_hazard_type(cls, v):
        allowed_types = ['flood', 'landslide', 'cyclone', 'earthquake']
        if v not in allowed_types:
            raise ValueError(f'Hazard type must be one of {allowed_types}')
        return v
    
    @validator('forecast_trend')
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

class HazardWithDetails(HazardResponse):
    """Extended hazard response with calculated details"""
    risk_factors: dict = Field(default_factory=dict, description="Breakdown of risk factors")
    recommended_action: str = Field(default="monitor", description="Recommended action based on risk")
    
    @classmethod
    def from_hazard(cls, hazard: HazardResponse):
        """Create extended response from base hazard"""
        risk_factors = {
            "rainfall_contribution": round(0.25 * min(hazard.rainfall / 100, 1.0) * 100, 2),
            "river_level_contribution": round(0.25 * min(hazard.river_level / 10, 1.0) * 100, 2),
            "elevation_risk": round(0.15 * (100 - min(hazard.elevation or 0, 100)), 2),
            "historical_contribution": round(0.15 * hazard.historical_risk, 2),
            "drainage_risk": round(0.10 * (100 - hazard.drainage_quality), 2),
            "trend_risk": round(0.10 * (20 if hazard.forecast_trend == "increasing" else 0), 2)
        }
        
        # Determine recommended action
        if hazard.risk_score >= 71:
            recommended_action = "immediate_evacuation"
        elif hazard.risk_score >= 51:
            recommended_action = "prepare_evacuation"
        elif hazard.risk_score >= 31:
            recommended_action = "monitor_closely"
        else:
            recommended_action = "monitor"
        
        return cls(
            **hazard.dict(),
            risk_factors=risk_factors,
            recommended_action=recommended_action
        )