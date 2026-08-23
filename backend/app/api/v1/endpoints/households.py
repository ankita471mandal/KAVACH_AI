from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.household import Household
from app.schemas.household import HouseholdResponse, HouseholdCreate

# CREATE ROUTER FIRST - This was missing!
router = APIRouter()

@router.get("/", response_model=List[HouseholdResponse])
def get_households(
    skip: int = 0,
    limit: int = 100,
    zone_id: int = None,
    db: Session = Depends(get_db)
):
    """Get all households"""
    query = db.query(Household)
    if zone_id:
        query = query.filter(Household.zone_id == zone_id)
    households = query.offset(skip).limit(limit).all()
    return households

@router.get("/{household_id}", response_model=HouseholdResponse)
def get_household(
    household_id: int,
    db: Session = Depends(get_db)
):
    """Get specific household"""
    household = db.query(Household).filter(Household.id == household_id).first()
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")
    return household

@router.get("/{household_id}/vulnerability")
def get_household_vulnerability(
    household_id: int,
    db: Session = Depends(get_db)
):
    """Get household vulnerability details"""
    household = db.query(Household).filter(Household.id == household_id).first()
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")
    
    reasons = []
    if household.elderly > 0:
        reasons.append("Elderly residents")
    if household.children > 0:
        reasons.append("Children present")
    if household.disabled > 0:
        reasons.append("Persons with disabilities")
    if household.medical_dependency:
        reasons.append("Medical dependency")
    if household.building_condition == "poor":
        reasons.append("Poor building condition")
    
    return {
        "household_id": household.id,
        "vulnerability_score": household.vulnerability_score,
        "reasons": reasons,
        "total_population": household.total_population
    }

@router.post("/", response_model=HouseholdResponse)
def create_household(
    household: HouseholdCreate,
    db: Session = Depends(get_db)
):
    """Create new household"""
    db_household = Household(**household.model_dump())
    
    # Calculate vulnerability
    vulnerability = calculate_vulnerability(db_household)
    db_household.vulnerability_score = vulnerability
    
    db.add(db_household)
    db.commit()
    db.refresh(db_household)
    return db_household

def calculate_vulnerability(household: Household) -> float:
    """Calculate vulnerability score"""
    score = 0
    
    # Age-based vulnerability
    if household.elderly > 0:
        score += 25
    if household.children > 0:
        score += 15
    
    # Disability
    if household.disabled > 0:
        score += 20
    
    # Medical
    if household.medical_dependency:
        score += 25
    
    # Building condition
    if household.building_condition == "poor":
        score += 15
    elif household.building_condition == "moderate":
        score += 8
    
    return min(score, 100.0)