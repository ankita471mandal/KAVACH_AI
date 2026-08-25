def rank_routes(routes, zone_risk_score=None):
    for route in routes:
        base_safety = route["properties"]["safety_score"]

        if zone_risk_score is None:
            route["properties"]["routing_safety_score"] = base_safety
        else:
            risk_safety = 100 - zone_risk_score

            route["properties"]["routing_safety_score"] = round(
                (base_safety + risk_safety) / 2,
                2
            )

    return sorted(
        routes,
        key=lambda route: (
            -route["properties"]["routing_safety_score"],
            route["properties"]["distance_km"]
        )
    )