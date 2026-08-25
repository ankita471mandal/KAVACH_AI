from routing.config import RISK_SCORE_THRESHOLD


def calculate_route_safety(risk_score):
    if risk_score is None:
        return None

    safety_score = 100 - risk_score

    if risk_score > RISK_SCORE_THRESHOLD:
        return 0

    return round(safety_score, 2)