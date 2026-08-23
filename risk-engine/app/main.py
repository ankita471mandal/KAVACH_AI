"""
FastAPI layer — thin routing only. All logic lives in the service files.
"""

from fastapi import FastAPI, HTTPException
from app.models import ZoneInput, RiskResponse
from app.risk_engine import (
    evaluate_zone,
    get_zone_input,
    get_all_zone_risks,
    apply_demo_scenario,
)
from app.explanation import build_explanation_text

app = FastAPI(
    title="Risk Calculation Engine — Member 1",
    description="Dynamic Red-Zone Engine for SIH Disaster Management project. "
                 "All data is DEMO/SIMULATION unless otherwise noted.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/risk", response_model=list[RiskResponse])
def get_all_risks():
    return get_all_zone_risks()


@app.get("/risk/{zone_id}", response_model=RiskResponse)
def get_risk_for_zone(zone_id: str):
    raw_input = get_zone_input(zone_id)
    if raw_input is None:
        raise HTTPException(status_code=404, detail=f"Zone '{zone_id}' not found")
    return evaluate_zone(raw_input)


@app.post("/risk/calculate", response_model=RiskResponse)
def calculate_custom_risk(raw_input: ZoneInput):
    """Lets other members submit raw data directly instead of using mock zones."""
    return evaluate_zone(raw_input)


@app.get("/zones/{zone_id}/explanation")
def get_zone_explanation(zone_id: str):
    raw_input = get_zone_input(zone_id)
    if raw_input is None:
        raise HTTPException(status_code=404, detail=f"Zone '{zone_id}' not found")
    result = evaluate_zone(raw_input)
    text = build_explanation_text(
        result.zone_id, result.risk_score, result.risk_level, result.main_drivers
    )
    return {"zone_id": zone_id, "explanation": text}


@app.post("/demo/{scenario_name}")
def run_demo_scenario(scenario_name: str):
    """Judge-demo endpoint: normal | heavy_rain | river_rising | extreme_flood"""
    success = apply_demo_scenario(scenario_name)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Unknown scenario. Use: normal, heavy_rain, river_rising, extreme_flood",
        )
    return {"message": f"Scenario '{scenario_name}' applied"}