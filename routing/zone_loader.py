import json
from pathlib import Path


ZONE_FILE = Path(__file__).parent.parent / "gis" / "data" / "zones.geojson"


def get_zones():
    with open(ZONE_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["features"]