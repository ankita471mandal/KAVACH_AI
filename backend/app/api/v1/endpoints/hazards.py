from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.hazard import Hazard
from app.schemas.hazard import HazardResponse, HazardCreate
from app.services.ml_service import MLService  # Import ML service

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
    """Create new hazard entry with ML-based risk calculation"""
    db_hazard = Hazard(**hazard.model_dump())
    
    # Use ML Service for risk calculation
    risk_score = MLService.calculate_hazard_risk(hazard.model_dump())
    db_hazard.risk_score = risk_score
    db_hazard.risk_level = get_risk_level(risk_score)
    
    db.add(db_hazard)
    db.commit()
    db.refresh(db_hazard)
    return db_hazard

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

@router.post("/ml-predict")
def predict_risk_ml(hazard_data: HazardCreate):
    """Direct ML prediction endpoint for testing"""
    risk_score = MLService.calculate_hazard_risk(hazard_data.model_dump())
    return {
        "risk_score": risk_score,
        "risk_level": get_risk_level(risk_score),
        "using_ml_model": True,
        "input_data": hazard_data.model_dump()
    }