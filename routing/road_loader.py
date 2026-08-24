import json
from pathlib import Path


ROADS_FILE = (
    Path(__file__).parent.parent
    / "gis"
    / "data"
    / "roads.geojson"
)


def load_roads():
    with open(ROADS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["features"]


def get_open_roads():
    roads = load_roads()

    return [
        road
        for road in roads
        if road["properties"]["status"] == "OPEN"
    ]