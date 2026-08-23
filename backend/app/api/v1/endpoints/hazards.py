from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.hazard import Hazard
from app.schemas.hazard import HazardResponse, HazardCreate

router = APIRouter()

@router.get("/live", response_model=List[HazardResponse])
def get_live_hazards(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all active hazards"""
    hazards = db.query(Hazard).offset(skip).limit(limit).all()
    return hazards

@router.post("/", response_model=HazardResponse)
def create_hazard(
    hazard: HazardCreate,
    db: Session = Depends(get_db)
):
    """Create new hazard entry"""
    db_hazard = Hazard(**hazard.model_dump())
    
    # Calculate risk score
    risk_score = calculate_risk_score(db_hazard)
    db_hazard.risk_score = risk_score
    db_hazard.risk_level = get_risk_level(risk_score)
    
    db.add(db_hazard)
    db.commit()
    db.refresh(db_hazard)
    return db_hazard

def calculate_risk_score(hazard: Hazard) -> float:
    """Calculate risk score based on multiple factors"""
    score = (
        0.25 * min(hazard.rainfall / 100, 1.0) * 100 +
        0.25 * min(hazard.river_level / 10, 1.0) * 100 +
        0.15 * (100 - min(hazard.elevation or 0, 100)) +
        0.15 * hazard.historical_risk +
        0.10 * (100 - hazard.drainage_quality) +
        0.10 * (20 if hazard.forecast_trend == "increasing" else 0)
    )
    return min(score, 100.0)

def get_risk_level(score: float) -> str:
    """Convert risk score to level"""
    if score >= 71:
        return "red"
    elif score >= 51:
        return "orange"
    elif score >= 31:
        return "yellow"
    else:
        return "green"