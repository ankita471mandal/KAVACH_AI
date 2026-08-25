import json
from pathlib import Path


ROUTES_FILE = (
    Path(__file__).parent.parent
    / "gis"
    / "data"
    / "routes.geojson"
)


def load_routes():
    with open(ROUTES_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["features"]


def get_active_routes():
    routes = load_routes()

    return [
        route
        for route in routes
        if route["properties"]["status"] == "ACTIVE"
    ]