from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.hospital import Hospital
from app.schemas.hospital import HospitalResponse, HospitalCreate, HospitalUpdate

router = APIRouter()

@router.get("/", response_model=List[HospitalResponse])
def get_hospitals(
    skip: int = 0,
    limit: int = 100,
    operational_only: bool = Query(False, description="Return only operational hospitals"),
    db: Session = Depends(get_db)
):
    """Get all hospitals"""
    query = db.query(Hospital)
    
    if operational_only:
        query = query.filter(Hospital.emergency_services == True)
    
    hospitals = query.offset(skip).limit(limit).all()
    return hospitals

@router.get("/{hospital_id}", response_model=HospitalResponse)
def get_hospital(
    hospital_id: int,
    db: Session = Depends(get_db)
):
    """Get specific hospital"""
    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital

@router.post("/", response_model=HospitalResponse)
def create_hospital(
    hospital: HospitalCreate,
    db: Session = Depends(get_db)
):
    """Create new hospital"""
    db_hospital = Hospital(**hospital.model_dump())
    
    # Calculate emergency capacity percentage
    if db_hospital.total_beds > 0:
        occupied = db_hospital.total_beds - db_hospital.available_beds
        db_hospital.emergency_capacity_percent = (occupied / db_hospital.total_beds) * 100
    
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

@router.put("/{hospital_id}", response_model=HospitalResponse)
def update_hospital(
    hospital_id: int,
    hospital_update: HospitalUpdate,
    db: Session = Depends(get_db)
):
    """Update hospital"""
    db_hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not db_hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    
    update_data = hospital_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_hospital, field, value)
    
    db.commit()
    db.refresh(db_hospital)
    return db_hospital