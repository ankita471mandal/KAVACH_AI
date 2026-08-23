from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import hazards, households, hospitals, shelters, roads, rescue, sos, zones
from app.db.init_db import init_db

# Initialize database
init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(hazards.router, prefix=f"{settings.API_V1_STR}/hazards", tags=["hazards"])
app.include_router(households.router, prefix=f"{settings.API_V1_STR}/households", tags=["households"])
app.include_router(shelters.router, prefix=f"{settings.API_V1_STR}/shelters", tags=["shelters"])
app.include_router(rescue.router, prefix=f"{settings.API_V1_STR}/rescue", tags=["rescue"])
app.include_router(sos.router, prefix=f"{settings.API_V1_STR}/sos", tags=["sos"])

@app.get("/")
def root():
    return {
        "message": "Kavach AI Backend API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)