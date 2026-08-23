"""
Normalization — converts raw values into a common 0-100 risk scale.
Never crashes on missing/invalid/out-of-range input.
"""

from typing import Optional
from app import config


def normalize(value, minimum: float, maximum: float) -> Optional[float]:
    """For factors where a HIGHER raw value means HIGHER risk."""
    if value is None:
        return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None

    if maximum == minimum:
        return 50.0  # degenerate range — neutral score, can't scale meaningfully

    if value < minimum:
        value = minimum
    elif value > maximum:
        value = maximum

    score = ((value - minimum) / (maximum - minimum)) * 100
    return round(score, 2)


def normalize_inverse(value, minimum: float, maximum: float) -> Optional[float]:
    """For factors where a LOWER raw value means HIGHER risk (e.g. elevation)."""
    score = normalize(value, minimum, maximum)
    if score is None:
        return None
    return round(100 - score, 2)


def normalize_factors(raw_data: dict) -> dict:
    """
    Normalizes every configured factor in raw_data using the correct
    direction (normal vs inverse) based on config.INVERSE_FACTORS.
    """
    normalized = {}
    for factor, bounds in config.RAW_RANGES.items():
        raw_value = raw_data.get(factor)
        if factor in config.INVERSE_FACTORS:
            normalized[factor] = normalize_inverse(raw_value, bounds["min"], bounds["max"])
        else:
            normalized[factor] = normalize(raw_value, bounds["min"], bounds["max"])
    return normalized