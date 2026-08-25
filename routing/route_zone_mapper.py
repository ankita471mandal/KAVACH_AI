from shapely.geometry import shape

from routing.zone_loader import get_zones


def map_route_to_zones(routes, zones):
    for route in routes:
        route_geometry = shape(route["geometry"])

        zone_ids = []

        for zone in zones:
            zone_geometry = shape(zone["geometry"])

            if route_geometry.intersects(zone_geometry):
                zone_id = zone["properties"]["zone_id"]
                zone_ids.append(zone_id)

        route["properties"]["zone_ids"] = zone_ids

    return routes


if __name__ == "__main__":
    from routing.route_loader import get_active_routes

    routes = get_active_routes()
    zones = get_zones()

    mapped_routes = map_route_to_zones(routes, zones)

    for route in mapped_routes:
        print(
            route["properties"]["route_id"],
            "->",
            route["properties"]["zone_ids"]
        )