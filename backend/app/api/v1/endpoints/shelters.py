from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.shelter import Shelter
from app.schemas.shelter import ShelterResponse

router = APIRouter()

@router.get("/", response_model=List[ShelterResponse])
def get_shelters(
    db: Session = Depends(get_db)
):
    """Get all shelters with capacity info"""
    shelters = db.query(Shelter).all()
    
    # Update safe capacity for each
    for shelter in shelters:
        shelter.safe_capacity = min(
            shelter.water_capacity,
            shelter.food_capacity,
            shelter.sanitation_capacity,
            shelter.medical_capacity,
            shelter.total_capacity
        )
        shelter.available_capacity = max(
            shelter.safe_capacity - shelter.current_occupancy,
            0
        )
    
    db.commit()
    return shelters

@router.get("/{shelter_id}/capacity")
def get_shelter_capacity(
    shelter_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed shelter capacity"""
    shelter = db.query(Shelter).filter(Shelter.id == shelter_id).first()
    if not shelter:
        raise HTTPException(status_code=404, detail="Shelter not found")
    
    safe_capacity = min(
        shelter.water_capacity,
        shelter.food_capacity,
        shelter.sanitation_capacity,
        shelter.medical_capacity,
        shelter.total_capacity
    )
    
    return {
        "shelter_id": shelter.id,
        "name": shelter.name,
        "total_capacity": shelter.total_capacity,
        "current_occupancy": shelter.current_occupancy,
        "safe_capacity": safe_capacity,
        "available_capacity": max(safe_capacity - shelter.current_occupancy, 0),
        "capacity_breakdown": {
            "water": shelter.water_capacity,
            "food": shelter.food_capacity,
            "sanitation": shelter.sanitation_capacity,
            "medical": shelter.medical_capacity,
            "physical": shelter.total_capacity
        }
    }