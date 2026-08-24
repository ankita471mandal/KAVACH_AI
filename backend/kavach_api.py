from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(
    title="Kavach AI Backend",
    description="Local integration backend for Kavach AI",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulationRequest(BaseModel):
    scenario: str = "heavy_rain"
    zone_id: str = "Z17"


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Kavach AI backend is running",
    }


@app.get("/health")
@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "Kavach AI Backend",
    }


@app.get("/zones")
@app.get("/api/zones")
def zones():
    return [
        {
            "id": "Z17",
            "zone_id": "Z17",
            "name": "Zone Z17",
            "risk_score": 48,
            "risk_level": "YELLOW",
            "population": 426,
            "vulnerable_households": 38,
        }
    ]


@app.get("/risk/{zone_id}")
@app.get("/api/risk/{zone_id}")
def zone_risk(zone_id: str):
    return {
        "zone_id": zone_id,
        "risk_score": 48,
        "risk_level": "YELLOW",
        "reasons": [
            "Moderate rainfall detected",
            "River level is rising",
            "Historical flood exposure exists",
            "Vulnerable households are present",
        ],
    }


@app.get("/households/{household_id}/vulnerability")
@app.get("/api/households/{household_id}/vulnerability")
def household_vulnerability(household_id: str):
    return {
        "household_id": household_id,
        "vulnerability_score": 91,
        "level": "CRITICAL",
        "reasons": [
            "Elderly resident",
            "Medical dependency",
            "Poor road accessibility",
            "High flood exposure",
        ],
    }


@app.get("/priority-areas")
@app.get("/api/priority-areas")
def priority_areas():
    return [
        {
            "zone_id": "Z17",
            "priority_score": 94,
            "priority_level": "IMMEDIATE",
            "people_at_risk": 146,
            "recommended_action": "Immediate assisted evacuation",
            "reasons": [
                "High flood exposure",
                "38 vulnerable households",
                "Medical dependency cases identified",
                "Risk is increasing",
            ],
        }
    ]


@app.post("/simulate")
@app.post("/api/simulate")
def simulate(request: SimulationRequest | None = None):
    zone_id = request.zone_id if request else "Z17"

    return {
        "success": True,
        "scenario": "heavy_rain",
        "zone_id": zone_id,
        "updated_risk_score": 87,
        "updated_risk_level": "RED",
        "message": "Heavy rain simulation applied successfully",
    }