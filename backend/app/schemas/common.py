from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar, List
from datetime import datetime

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response"""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

class MessageResponse(BaseModel):
    """Simple message response"""
    message: str
    success: bool = True

class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    database: str = "connected"
    version: str = "1.0.0"

class LocationRequest(BaseModel):
    """Location request schema"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class DistanceCalculation(BaseModel):
    """Distance calculation result"""
    from_lat: float
    from_lng: float
    to_lat: float
    to_lng: float
    distance_km: float
    estimated_time_minutes: Optional[int] = None