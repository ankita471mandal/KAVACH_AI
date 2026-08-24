from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.zone import Zone
from app.schemas.zone import ZoneResponse, ZoneCreate, ZoneUpdate

router = APIRouter()

@router.get("/", response_model=List[ZoneResponse])
def get_zones(
    skip: int = 0,
    limit: int = 100,
    risk_level: Optional[str] = Query(None, description="Filter by risk level"),
    db: Session = Depends(get_db)
):
    """Get all zones"""
    query = db.query(Zone)
    
    if risk_level:
        query = query.filter(Zone.risk_level == risk_level)
    
    zones = query.offset(skip).limit(limit).all()
    return zones

@router.get("/{zone_id}", response_model=ZoneResponse)
def get_zone(
    zone_id: int,
    db: Session = Depends(get_db)
):
    """Get specific zone"""
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return zone

@router.post("/", response_model=ZoneResponse)
def create_zone(
    zone: ZoneCreate,
    db: Session = Depends(get_db)
):
    """Create new zone"""
    db_zone = Zone(**zone.model_dump())
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone

@router.get("/priority/list")
def get_priority_zones(
    db: Session = Depends(get_db)
):
    """Get priority zones ordered by priority score"""
    zones = db.query(Zone).order_by(Zone.priority_score.desc()).all()
    
    priority_list = []
    for zone in zones:
        if zone.priority_score >= 70:
            priority_list.append({
                "zone_id": zone.id,
                "zone_name": zone.name,
                "priority_score": zone.priority_score,
                "priority_level": zone.priority_level,
                "risk_score": zone.risk_score,
                "vulnerable_population": zone.vulnerable_population,
                "action": "immediate_evacuation" if zone.risk_score >= 71 else "prepare_evacuation"
            })
    
    return {
        "priority_zones": priority_list,
        "total_high_priority": len(priority_list),
        "timestamp": "2024-01-15T10:30:00Z"
    }