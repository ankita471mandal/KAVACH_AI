from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.session import get_db
from app.models.rescue_report import RescueReport
from app.schemas.rescue import RescueReportCreate, RescueReportResponse

router = APIRouter()

@router.post("/report", response_model=RescueReportResponse)
def submit_rescue_report(
    report: RescueReportCreate,
    db: Session = Depends(get_db)
):
    """Submit rescue team report - TRIGGERS SYSTEM RECALCULATION"""
    db_report = RescueReport(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    # TRIGGER RECALCULATION
    if report.report_type == "road_blocked":
        trigger_road_update(report, db)
    
    return db_report

def trigger_road_update(report: RescueReportCreate, db: Session):
    """Update road status when blocked"""
    from app.models.road import Road
    
    # Find nearby road
    # Simplified: In production, use geospatial query
    road = db.query(Road).first()  # Replace with actual logic
    
    if road:
        road.status = "BLOCKED"
        road.last_updated_by = report.reporter_name
        road.verified = True
        db.commit()
        
        # Trigger route recalculation (handled by Member 5)
        print(f"⚠️  Road {road.name} marked as BLOCKED - Routes need recalculation")

@router.get("/reports", response_model=List[RescueReportResponse])
def get_rescue_reports(
    verified: bool = None,
    db: Session = Depends(get_db)
):
    """Get rescue reports"""
    query = db.query(RescueReport)
    if verified is not None:
        query = query.filter(RescueReport.verified == verified)
    return query.all()