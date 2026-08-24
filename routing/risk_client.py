import requests

from routing.config import RISK_API_BASE_URL


def get_all_risks():
    response = requests.get(
        f"{RISK_API_BASE_URL}/risk",
        timeout=5
    )

    response.raise_for_status()

    return response.json()


def get_zone_risk(zone_id):
    response = requests.get(
        f"{RISK_API_BASE_URL}/risk/{zone_id}",
        timeout=5
    )

    response.raise_for_status()

    return response.json()
if __name__ == "__main__":
    print(get_all_risks())