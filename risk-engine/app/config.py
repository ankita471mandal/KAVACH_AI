"""
Configuration for the Risk Calculation Engine.

IMPORTANT: All weights, ranges, and thresholds below are PROTOTYPE
ASSUMPTIONS for a 48-hour hackathon build. They are NOT official
disaster-management standards. In a real deployment these would be
calibrated using historical flood data and validated with domain
experts (hydrologists, disaster management authorities).
"""

# ---------------------------------------------------------------------------
# Risk factor weights — must sum to 1.0
# ---------------------------------------------------------------------------
WEIGHTS = {
    "rainfall": 0.25,
    "river_level": 0.25,
    "elevation": 0.15,
    "historical_risk": 0.15,
    "drainage": 0.10,
    "trend": 0.10,
}

FACTOR_LABELS = {
    "rainfall": "Rainfall Intensity",
    "river_level": "River/Water Level",
    "elevation": "Elevation Susceptibility",
    "historical_risk": "Historical Hazard Risk",
    "drainage": "Drainage Vulnerability",
    "trend": "Forecast Trend",
}

# Raw input ranges used to normalize values to 0-100
RAW_RANGES = {
    "rainfall":        {"min": 0,   "max": 300},  # mm in 24h
    "river_level":     {"min": 0,   "max": 10},   # meters above normal
    "elevation":       {"min": 0,   "max": 500},  # meters
    "historical_risk": {"min": 0,   "max": 100},  # pre-scored hazard index
    "drainage":        {"min": 0,   "max": 100},  # vulnerability index (higher = worse)
    "trend":           {"min": -50, "max": 50},   # forecast % change
}

# Factors where a LOWER raw value means HIGHER risk (use normalize_inverse for these)
INVERSE_FACTORS = {"elevation"}

REQUIRED_FIELDS = list(RAW_RANGES.keys())

# Classification thresholds (inclusive ranges) — prototype values, validate before real use
CLASSIFICATION_THRESHOLDS = [
    (0, 30, "LOW"),
    (31, 50, "MODERATE"),
    (51, 70, "HIGH"),
    (71, 100, "CRITICAL"),
]

# Trend classification thresholds
TREND_RAPIDLY_RISING = 15
TREND_RISING = 5
TREND_STABLE_BAND = 4      # -4 to +4 is STABLE
TREND_DECREASING = -5

TOP_N_DRIVERS = 3

DATA_FRESHNESS_MAX_MINUTES = 60