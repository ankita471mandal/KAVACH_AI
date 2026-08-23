"""
Risk trend — compares current risk score to the previous one.
"""

from typing import Optional, Tuple
from app import config


def calculate_trend(
    previous_score: Optional[float],
    current_score: Optional[float],
) -> Tuple[Optional[float], str]:
    if previous_score is None or current_score is None:
        return None, "UNKNOWN"

    change = round(current_score - previous_score, 2)

    if change >= config.TREND_RAPIDLY_RISING:
        label = "RAPIDLY_RISING"
    elif change >= config.TREND_RISING:
        label = "RISING"
    elif -config.TREND_STABLE_BAND <= change <= config.TREND_STABLE_BAND:
        label = "STABLE"
    elif change <= config.TREND_DECREASING:
        label = "DECREASING"
    else:
        label = "STABLE"

    return change, label