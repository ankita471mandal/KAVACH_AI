"""
Orchestrator — ties normalization -> calculation -> classification ->
trend -> confidence -> explanation into a single RiskResponse.
Also loads and manages mock zone data for demo/simulation mode.
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app import config
from app.models import ZoneInput, RiskResponse
from app.normalization import normalize_factors
from app.classification import classify_risk
from app.trend import calculate_trend
from app.confidence import calculate_data_confidence
from app.explanation import generate_explanation

# ---------------------------------------------------------------------------
# DEMO / SIMULATION DATA — loaded once at startup. NOT real sensor data.
# ---------------------------------------------------------------------------
_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_zones.json"


def _load_sample_zones() -> Dict[str, dict]:
    with open(_DATA_PATH, "r") as f:
        zones_list = json.load(f)
    return {z["zone_id"]: z for z in zones_list}


MOCK_ZONES: Dict[str, dict] = _load_sample_zones()

DEMO_SCENARIOS = {
    "normal": {},
    "heavy_rain": {"rainfall": 220, "trend": 20},
    "river_rising": {"river_level": 8.5, "trend": 25},
    "extreme_flood": {"rainfall": 280, "river_level": 9.5, "drainage": 90, "trend": 40},
}


def apply_demo_scenario(scenario_name: str) -> bool:
    """Mutates MOCK_ZONES in place to simulate changing conditions."""
    changes = DEMO_SCENARIOS.get(scenario_name)
    if changes is None:
        return False
    for zone_data in MOCK_ZONES.values():
        zone_data.update(changes)
        zone_data["timestamp"] = datetime.now(timezone.utc).isoformat()
    return True


def get_zone_input(zone_id: str) -> Optional[ZoneInput]:
    zone_data = MOCK_ZONES.get(zone_id)
    if zone_data is None:
        return None
    return ZoneInput(**zone_data)


# ---------------------------------------------------------------------------
# CORE CALCULATION
# ---------------------------------------------------------------------------
def calculate_risk_score(normalized_scores: dict) -> Optional[float]:
    available = {k: v for k, v in normalized_scores.items() if v is not None}
    if not available:
        return None

    total_weight = sum(config.WEIGHTS[k] for k in available)
    if total_weight == 0:
        return None

    weighted_sum = sum(config.WEIGHTS[k] * v for k, v in available.items())
    return round(weighted_sum / total_weight, 2)


def evaluate_zone(raw_input: ZoneInput) -> RiskResponse:
    raw_dict = raw_input.model_dump()

    normalized = normalize_factors(raw_dict)
    risk_score = calculate_risk_score(normalized)
    risk_level = classify_risk(risk_score)
    trend_change, trend_label = calculate_trend(raw_input.previous_risk_score, risk_score)
    completeness, missing_fields = calculate_data_confidence(raw_dict)
    main_drivers = generate_explanation(normalized)

    timestamp = raw_input.timestamp or datetime.now(timezone.utc)

    return RiskResponse(
        zone_id=raw_input.zone_id,
        timestamp=timestamp,
        risk_score=risk_score,
        risk_level=risk_level,
        risk_trend=trend_label,
        risk_trend_change=trend_change,
        data_confidence=completeness,
        missing_fields=missing_fields,
        factor_scores=normalized,
        main_drivers=main_drivers,
        is_demo_data=True,
    )


def get_all_zone_risks() -> List[RiskResponse]:
    return [evaluate_zone(ZoneInput(**zone_data)) for zone_data in MOCK_ZONES.values()]