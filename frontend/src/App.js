import React, { useEffect, useState } from 'react';
import ApiService from './services/api';
import './App.css';

function App() {
  const [health, setHealth] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [healthRes, statsRes] = await Promise.all([
        ApiService.getHealth(),
        ApiService.getStats()
      ]);
      
      setHealth(healthRes.data);
      setStats(statsRes.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to connect to backend. Make sure it is running on http://localhost:8000');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="App">
        <header className="App-header">
          <h1>🔄 Loading Kavach AI...</h1>
        </header>
      </div>
    );
  }

  if (error) {
    return (
      <div className="App">
        <header className="App-header">
          <h1>❌ Connection Error</h1>
          <p>{error}</p>
          <button onClick={loadData}>Retry</button>
        </header>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>🚨 Kavach AI - Disaster Management System</h1>
        
        <div className="status-card">
          <h2>System Status</h2>
          <p>Backend: {health?.status === 'healthy' ? '✅ Online' : '❌ Offline'}</p>
          <p>Database: {health?.database === 'connected' ? '✅ Connected' : '❌ Disconnected'}</p>
          <p>API Version: {health?.api_version || 'N/A'}</p>
        </div>

        {stats && (
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Zones</h3>
              <p className="stat-value">{stats.total_zones}</p>
            </div>
            <div className="stat-card">
              <h3>Hospitals</h3>
              <p className="stat-value">{stats.total_hospitals}</p>
            </div>
            <div className="stat-card">
              <h3>Shelters</h3>
              <p className="stat-value">{stats.total_shelters}</p>
            </div>
            <div className="stat-card red">
              <h3>Red Zones</h3>
              <p className="stat-value">{stats.red_zones}</p>
            </div>
          </div>
        )}

        <div className="actions">
          <button onClick={() => window.open('http://localhost:8000/docs', '_blank')}>
            📖 View API Documentation
          </button>
        </div>
      </header>
    </div>
  );
}

export default App;