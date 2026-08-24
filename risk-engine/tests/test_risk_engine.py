from app.models import ZoneInput
from app.risk_engine import evaluate_zone, get_all_zone_risks, calculate_risk_score


def test_low_risk_zone():
    raw = ZoneInput(
        zone_id="TEST_LOW", rainfall=10, river_level=0.5, elevation=450,
        historical_risk=5, drainage=5, trend=-10,
    )
    result = evaluate_zone(raw)
    assert result.risk_level in ["LOW", "MODERATE"]

def test_critical_risk_zone():
    raw = ZoneInput(
        zone_id="TEST_CRIT", rainfall=290, river_level=9.5, elevation=10,
        historical_risk=95, drainage=95, trend=45,
    )
    result = evaluate_zone(raw)
    assert result.risk_level == "CRITICAL"

def test_missing_data_does_not_crash():
    raw = ZoneInput(zone_id="TEST_MISSING", rainfall=100)
    result = evaluate_zone(raw)
    assert result.risk_score is not None
    assert result.data_confidence < 100

def test_all_data_missing_returns_unknown():
    raw = ZoneInput(zone_id="TEST_EMPTY")
    result = evaluate_zone(raw)
    assert result.risk_score is None
    assert result.risk_level == "UNKNOWN"

def test_trend_rapidly_rising():
    raw = ZoneInput(
        zone_id="Z17", rainfall=150, river_level=6.5, elevation=40,
        historical_risk=60, drainage=75, trend=18, previous_risk_score=30,
    )
    result = evaluate_zone(raw)
    assert result.risk_trend in ["RISING", "RAPIDLY_RISING"]

def test_calculate_risk_score_all_missing():
    assert calculate_risk_score({k: None for k in
        ["rainfall", "river_level", "elevation", "historical_risk", "drainage", "trend"]}) is None

def test_multiple_zones():
    results = get_all_zone_risks()
    assert len(results) == 4
    zone_ids = {r.zone_id for r in results}
    assert zone_ids == {"Z01", "Z02", "Z04", "Z17"}