"""
Risk classification. Thresholds are configurable in config.py —
never hard-code them elsewhere.
"""

from typing import Optional
from app import config


def classify_risk(risk_score: Optional[float]) -> str:
    if risk_score is None:
        return "UNKNOWN"

    for low, high, label in config.CLASSIFICATION_THRESHOLDS:
        if low <= risk_score <= high:
            return label

    return "UNKNOWN"