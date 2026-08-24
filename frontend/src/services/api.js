const API_BASE_URL = "http://127.0.0.1:8000";

// Example of how your fetch calls should look:
export const api = {
  health: () => fetch(`${API_BASE_URL}/health`).then(res => res.json()),
  zones: () => fetch(`${API_BASE_URL}/zones`).then(res => res.json()),
  risk: (zoneId) => fetch(`${API_BASE_URL}/risk/${zoneId}`).then(res => res.json()),
  vulnerability: (id) => fetch(`${API_BASE_URL}/households/${id}/vulnerability`).then(res => res.json()),
  priorityAreas: () => fetch(`${API_BASE_URL}/priority-areas`).then(res => res.json()),
  simulate: () => fetch(`${API_BASE_URL}/simulate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ scenario: "heavy_rain", zone_id: "Z17" })
  }).then(res => res.json()),
};