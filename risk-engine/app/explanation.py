"""
Explainable risk — answers "WHY is this zone at this risk level?"
"""

from typing import Dict, List
from app import config


def generate_explanation(normalized_scores: Dict[str, float]) -> List[str]:
    """
    Ranks factors by their weighted contribution to the risk score and
    returns the top N as human-readable labels.
    """
    contributions = {}
    for factor, score in normalized_scores.items():
        if score is None:
            continue
        contributions[factor] = config.WEIGHTS[factor] * score

    ranked = sorted(contributions.items(), key=lambda item: item[1], reverse=True)
    top_factors = [factor for factor, _ in ranked[: config.TOP_N_DRIVERS]]

    return [config.FACTOR_LABELS.get(f, f) for f in top_factors]


def build_explanation_text(
    zone_id: str, risk_score: float, risk_level: str, main_drivers: List[str]
) -> str:
    """Builds a plain-English sentence for the /explanation endpoint."""
    if not main_drivers:
        return f"Zone {zone_id} has insufficient data to identify main risk drivers."

    drivers_text = ", ".join(main_drivers)
    return (
        f"Zone {zone_id} is classified as {risk_level} "
        f"(risk score: {risk_score}). Main contributing factors: {drivers_text}."
    )