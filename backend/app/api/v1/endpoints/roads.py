from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.road import Road
from app.schemas.road import RoadResponse, RoadCreate, RoadUpdate

router = APIRouter()

@router.get("/", response_model=List[RoadResponse])
def get_roads(
    status: str = None,
    db: Session = Depends(get_db)
):
    """Get all roads"""
    query = db.query(Road)
    if status:
        query = query.filter(Road.status == status)
    return query.all()

@router.get("/{road_id}", response_model=RoadResponse)
def get_road(
    road_id: int,
    db: Session = Depends(get_db)
):
    """Get specific road"""
    road = db.query(Road).filter(Road.id == road_id).first()
    if not road:
        raise HTTPException(status_code=404, detail="Road not found")
    return road

@router.post("/", response_model=RoadResponse)
def create_road(
    road: RoadCreate,
    db: Session = Depends(get_db)
):
    """Create new road"""
    db_road = Road(**road.model_dump())
    db.add(db_road)
    db.commit()
    db.refresh(db_road)
    return db_road

@router.put("/{road_id}/status")
def update_road_status(
    road_id: int,
    status: str,
    updated_by: str,
    db: Session = Depends(get_db)
):
    """Update road status (called by rescue teams)"""
    road = db.query(Road).filter(Road.id == road_id).first()
    if not road:
        raise HTTPException(status_code=404, detail="Road not found")
    
    old_status = road.status
    road.status = status
    road.last_updated_by = updated_by
    road.verified = True
    
    db.commit()
    
    return {
        "message": "Road status updated",
        "road_id": road_id,
        "old_status": old_status,
        "new_status": status,
        "updated_by": updated_by,
        "trigger_recalculation": True if status == "BLOCKED" else False
    }