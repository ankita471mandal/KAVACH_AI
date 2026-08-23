"""
Pydantic schemas — the data contract for this module.
ZoneInput  = what goes IN (raw values; any field can be missing)
RiskResponse = what comes OUT (consumed by Members 2, 4, 5, 6)
"""

from typing import Optional, Dict, List
from datetime import datetime
from pydantic import BaseModel


class ZoneInput(BaseModel):
    zone_id: str
    timestamp: Optional[datetime] = None

    rainfall: Optional[float] = None
    river_level: Optional[float] = None
    elevation: Optional[float] = None
    historical_risk: Optional[float] = None
    drainage: Optional[float] = None
    trend: Optional[float] = None

    # needed to compute risk TREND against the last known score
    previous_risk_score: Optional[float] = None


class RiskResponse(BaseModel):
    zone_id: str
    timestamp: datetime
    risk_score: Optional[float]
    risk_level: str
    risk_trend: str
    risk_trend_change: Optional[float]
    data_confidence: float
    missing_fields: List[str]
    factor_scores: Dict[str, Optional[float]]
    main_drivers: List[str]
    is_demo_data: bool = True