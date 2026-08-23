from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class HouseholdBase(BaseModel):
    location_lat: float
    location_lng: float
    total_population: int = 0
    children: int = 0
    elderly: int = 0
    disabled: int = 0
    medical_dependency: bool = False
    medical_details: Optional[str] = None
    building_condition: str = "good"
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None

class HouseholdCreate(HouseholdBase):
    pass

class HouseholdUpdate(BaseModel):
    total_population: Optional[int] = None
    children: Optional[int] = None
    elderly: Optional[int] = None
    disabled: Optional[int] = None
    medical_dependency: Optional[bool] = None
    building_condition: Optional[str] = None

class HouseholdResponse(HouseholdBase):
    id: int
    vulnerability_score: float
    zone_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True