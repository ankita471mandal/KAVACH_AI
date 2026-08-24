# Risk Calculation Engine — Member 1
### Smart India Hackathon: Hazard-Based Red Zone Identification

## Module Description
This module calculates flood-disaster risk per geographic zone, classifies
it, tracks trend over time, reports data confidence, and explains WHY a
zone is high-risk. It exposes this via a REST API for the rest of the team.

## Architecture
Raw input → Normalization → Weighted Risk Score → Classification → Trend →
Confidence → Explanation → JSON API response. See `app/risk_engine.py` for
the orchestration logic; each step is a separate, independently testable file.

## Risk Formula
Risk = 0.25×Rainfall + 0.25×River Level + 0.15×Elevation
+ 0.15×Historical Risk + 0.10×Drainage + 0.10×Trend
All factors normalized to 0–100 first. **These weights and the LOW/
MODERATE/HIGH/CRITICAL thresholds are prototype assumptions only** —
not official disaster-management standards. They should be calibrated
with historical data and domain experts before real deployment.

## Installation
```powershell
pip install -r requirements.txt
```

## Running
```powershell
uvicorn app.main:app --reload
```
Visit http://127.0.0.1:8000/docs for interactive Swagger docs.

## Testing
```powershell
pytest
```

## Demo Mode
`POST /demo/{scenario_name}` where scenario is one of:
`normal`, `heavy_rain`, `river_rising`, `extreme_flood`.
This mutates the in-memory DEMO data only — **never real sensor data**.

## Sample API Response — `GET /risk/Z17`
```json
{
  "zone_id": "Z17",
  "risk_score": 62.3,
  "risk_level": "HIGH",
  "risk_trend": "RISING",
  "data_confidence": 100,
  "factor_scores": {"rainfall": 50, "river_level": 65, "elevation": 92},
  "main_drivers": ["Elevation Susceptibility", "River/Water Level", "Rainfall Intensity"]
}
```

## Limitations
- All data is simulated/demo, not live sensor feeds.
- Weights and thresholds are unvalidated prototype values.
- No ML — intentionally simple and explainable for a 48-hour build.
- Not suitable for real emergency deployment without calibration.

## Future Real-Data Integration
Rainfall/river level → weather & hydrology APIs; elevation → GIS/DEM data;
historical risk → disaster records; all would need authoritative-source
validation before replacing mock data.