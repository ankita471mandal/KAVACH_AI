from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import (
    hazards, 
    households, 
    hospitals, 
    shelters, 
    roads, 
    rescue, 
    sos, 
    zones
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Kavach AI - Real-Time Disaster Management System",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(hazards.router, prefix=f"{settings.API_V1_STR}/hazards", tags=["Hazards"])
app.include_router(households.router, prefix=f"{settings.API_V1_STR}/households", tags=["Households"])
app.include_router(hospitals.router, prefix=f"{settings.API_V1_STR}/hospitals", tags=["Hospitals"])
app.include_router(shelters.router, prefix=f"{settings.API_V1_STR}/shelters", tags=["Shelters"])
app.include_router(roads.router, prefix=f"{settings.API_V1_STR}/roads", tags=["Roads"])
app.include_router(zones.router, prefix=f"{settings.API_V1_STR}/zones", tags=["Zones"])
app.include_router(rescue.router, prefix=f"{settings.API_V1_STR}/rescue", tags=["Rescue"])
app.include_router(sos.router, prefix=f"{settings.API_V1_STR}/sos", tags=["SOS"])

@app.get("/")
def root():
    return {
        "message": "Kavach AI Backend API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "api": "/api/v1"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "api_version": "v1"
    }

@app.get("/stats")
def get_stats():
    """Get system statistics"""
    from app.db.session import SessionLocal
    from app.models import Zone, Hospital, Shelter, Household
    
    db = SessionLocal()
    try:
        return {
            "total_zones": db.query(Zone).count(),
            "total_hospitals": db.query(Hospital).count(),
            "total_shelters": db.query(Shelter).count(),
            "total_households": db.query(Household).count(),
            "red_zones": db.query(Zone).filter(Zone.risk_level == "red").count(),
            "high_priority_zones": db.query(Zone).filter(Zone.priority_score >= 70).count()
        }
    finally:
        db.close()