from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.sos_request import SOSRequest
from app.schemas.sos import SOSCreate, SOSResponse

router = APIRouter()

@router.post("/", response_model=SOSResponse)
def create_sos(
    sos: SOSCreate,
    db: Session = Depends(get_db)
):
    """Create SOS request"""
    db_sos = SOSRequest(**sos.dict())
    
    # Auto-prioritize based on emergency type
    if sos.emergency_type == "MEDICAL":
        db_sos.priority = "CRITICAL"
    elif sos.emergency_type == "TRAPPED":
        db_sos.priority = "HIGH"
    else:
        db_sos.priority = "MEDIUM"
    
    db.add(db_sos)
    db.commit()
    db.refresh(db_sos)
    
    print(f"🆘 SOS Request #{db_sos.id} - {db_sos.emergency_type} - Priority: {db_sos.priority}")
    
    return db_sos

@router.get("/", response_model=List[SOSResponse])
def get_sos_requests(
    status: str = None,
    db: Session = Depends(get_db)
):
    """Get SOS requests"""
    query = db.query(SOSRequest)
    if status:
        query = query.filter(SOSRequest.status == status)
    return query.order_by(SOSRequest.created_at.desc()).all()