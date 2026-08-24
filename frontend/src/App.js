import { useEffect, useState } from "react";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [backendStatus, setBackendStatus] = useState("Connecting...");
  const [zones, setZones] = useState([]);
  const [priorityAreas, setPriorityAreas] = useState([]);
  const [selectedRisk, setSelectedRisk] = useState(null);
  const [vulnerability, setVulnerability] = useState(null);
  const [simulationResult, setSimulationResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const checkBackend = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/health`);
      if (res.ok) {
        setBackendStatus("✅ Connected");
        loadData();
      } else {
        setBackendStatus("❌ Failed");
      }
    } catch (err) {
      setBackendStatus("❌ Connection Failed");
      setError("Cannot reach backend at http://127.0.0.1:8000");
    } finally {
      setLoading(false);
    }
  };

  const loadData = async () => {
    try {
      const [zonesRes, priorityRes] = await Promise.all([
        fetch(`${API_BASE_URL}/zones`),
        fetch(`${API_BASE_URL}/priority-areas`)
      ]);

      setZones(await zonesRes.json());
      setPriorityAreas(await priorityRes.json());
    } catch (err) {
      setError("Failed to load data");
    }
  };

  const loadRisk = async (zoneId) => {
    try {
      const res = await fetch(`${API_BASE_URL}/risk/${zoneId}`);
      setSelectedRisk(await res.json());
    } catch (err) {
      setError("Failed to load risk data");
    }
  };

  const loadVulnerability = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/households/H102/vulnerability`);
      setVulnerability(await res.json());
    } catch (err) {
      setError("Failed to load vulnerability");
    }
  };

  const simulateHeavyRain = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/simulate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenario: "heavy_rain", zone_id: "Z17" })
      });
      const data = await res.json();
      setSimulationResult(data);
      loadData(); // refresh data
    } catch (err) {
      setError("Simulation failed");
    }
  };

  useEffect(() => {
    checkBackend();
  }, []);

  if (loading) return <div className="loading">Loading Kavach AI...</div>;

  return (
    <div className="app">
      <header className="header">
        <h1>🛡️ KAVACH AI</h1>
        <p>Real-Time Disaster Intelligence System</p>
        <p className="status">Backend Status: {backendStatus}</p>
      </header>

      {error && <div className="error">{error}</div>}

      <div className="actions">
        <button onClick={simulateHeavyRain}>🌧️ Simulate Heavy Rain</button>
        <button onClick={loadVulnerability}>👥 Show Household H102 Vulnerability</button>
      </div>

      {simulationResult && (
        <div className="card success">
          <h2>Simulation Result</h2>
          <p>{simulationResult.message}</p>
          <p>Risk Updated to: <strong>{simulationResult.updated_risk_score}</strong> (RED)</p>
        </div>
      )}

      <div className="grid">
        <div className="card">
          <h2>Zones</h2>
          {zones.map(z => (
            <button key={z.id} className="zone-btn" onClick={() => loadRisk(z.id)}>
              {z.name} — Risk: {z.risk_score} ({z.risk_level})
            </button>
          ))}
        </div>

        <div className="card">
          <h2>Priority Areas</h2>
          {priorityAreas.map(p => (
            <div key={p.zone_id} className="priority">
              <h3>🔴 {p.zone_id} — Priority {p.priority_score}</h3>
              <p><strong>Action:</strong> {p.recommended_action}</p>
              <ul>
                {p.reasons?.map(r => <li key={r}>✓ {r}</li>)}
              </ul>
            </div>
          ))}
        </div>
      </div>

      {selectedRisk && (
        <div className="card">
          <h2>Risk Details - {selectedRisk.zone_id}</h2>
          <p>Risk Score: <strong>{selectedRisk.risk_score}</strong></p>
          <ul>
            {selectedRisk.reasons?.map(r => <li key={r}>✓ {r}</li>)}
          </ul>
        </div>
      )}

      {vulnerability && (
        <div className="card danger">
          <h2>Household H102 - Vulnerability</h2>
          <p>Score: <strong>{vulnerability.vulnerability_score}</strong> (CRITICAL)</p>
          <ul>
            {vulnerability.reasons?.map(r => <li key={r}>✓ {r}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;