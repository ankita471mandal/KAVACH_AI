def build_risk_lookup(risk_data):
    return {
        item["zone_id"]: item["risk_score"]
        for item in risk_data
        if item.get("risk_score") is not None
    }


def get_route_risk(route, risk_lookup):
    zone_ids = route["properties"].get("zone_ids", [])

    zone_risks = [
        risk_lookup[zone_id]
        for zone_id in zone_ids
        if zone_id in risk_lookup
    ]

    if not zone_risks:
        return None

    return max(zone_risks)