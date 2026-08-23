import json
from pathlib import Path


DATA_FILE = Path(__file__).parent.parent / "data" / "zones.geojson"


def load_zones():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def validate_zones(data):
    if data.get("type") != "FeatureCollection":
        raise ValueError("Invalid GeoJSON: expected FeatureCollection")

    features = data.get("features", [])

    print(f"Total zones: {len(features)}")

    for feature in features:
        properties = feature.get("properties", {})

        zone_id = properties.get("zone_id")
        risk_score = properties.get("risk_score")
        risk_level = properties.get("risk_level")

        print(
            f"Zone: {zone_id} | "
            f"Risk: {risk_score} | "
            f"Level: {risk_level}"
        )


if __name__ == "__main__":
    zones = load_zones()
    validate_zones(zones)