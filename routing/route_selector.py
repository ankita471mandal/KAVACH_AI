from routing.route_loader import get_active_routes
from routing.route_ranker import rank_routes
from routing.risk_client import get_all_risks


def select_best_route():

    routes = get_active_routes()

    if not routes:
        return None

    risks = get_all_risks()

    if not risks:
        return rank_routes(routes)[0]

    risk_score = risks[0].get("risk_score")

    ranked_routes = rank_routes(routes, risk_score)

    return ranked_routes[0]


if __name__ == "__main__":
    best_route = select_best_route()

    if best_route:
        print("Best route:")
        print(best_route)
    else:
        print("No active route available.")