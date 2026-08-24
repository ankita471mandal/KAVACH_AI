"""
Data confidence / input completeness — NOT a probability of correctness.
Also flags stale data.
"""

from datetime import datetime, timezone
from typing import List, Optional, Tuple
from app import config


def calculate_data_confidence(raw_data: dict) -> Tuple[float, List[str]]:
    """Returns (completeness_percentage, list_of_missing_field_names)."""
    required = config.REQUIRED_FIELDS
    missing = [f for f in required if raw_data.get(f) is None]
    available_count = len(required) - len(missing)
    completeness = round((available_count / len(required)) * 100, 2)
    return completeness, missing


def check_data_freshness(timestamp: Optional[datetime]) -> bool:
    """Returns True if data is considered STALE."""
    if timestamp is None:
        return True

    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    age_minutes = (datetime.now(timezone.utc) - timestamp).total_seconds() / 60
    return age_minutes > config.DATA_FRESHNESS_MAX_MINUTES