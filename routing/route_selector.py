from routing.route_loader import get_active_routes
from routing.route_ranker import rank_routes
from routing.risk_client import get_all_risks
from routing.zone_loader import get_zones
from routing.route_zone_mapper import map_route_to_zones
from routing.risk_mapping import build_risk_lookup, get_route_risk


def select_best_route():

    routes = get_active_routes()

    if not routes:
        return None

    risks = get_all_risks()
    zones = get_zones()

    routes = map_route_to_zones(routes, zones)

    risk_lookup = build_risk_lookup(risks)

    # Calculate risk-aware safety for every route
    for route in routes:
        route_risk = get_route_risk(route, risk_lookup)

        route["properties"]["zone_risk_score"] = route_risk

    # Rank routes using base safety + zone risk
    ranked_routes = []

    for route in routes:
        route_risk = route["properties"]["zone_risk_score"]

        ranked = rank_routes([route], route_risk)

        ranked_routes.append(ranked[0])

    ranked_routes.sort(
        key=lambda route: (
            -route["properties"]["routing_safety_score"],
            route["properties"]["distance_km"]
        )
    )

    return ranked_routes[0]


if __name__ == "__main__":
    best_route = select_best_route()

    if best_route:
        print("Best route:")
        print(best_route)
    else:
        print("No active route available.")