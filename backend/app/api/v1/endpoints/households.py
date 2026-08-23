from app.services.ml_service import MLService

# ... existing imports ...

@router.post("/", response_model=HouseholdResponse)
def create_household(
    household: HouseholdCreate,
    db: Session = Depends(get_db)
):
    """Create new household with ML-based vulnerability"""
    db_household = Household(**household.model_dump())
    
    # Use ML Service for vulnerability calculation
    vulnerability = MLService.calculate_household_vulnerability(household.model_dump())
    db_household.vulnerability_score = vulnerability
    
    db.add(db_household)
    db.commit()
    db.refresh(db_household)
    return db_household