import React, { useEffect, useState } from 'react';
import apiService from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [priorityZones, setPriorityZones] = useState([]);
  const [shelterAlerts, setShelterAlerts] = useState([]);
  const [sosRequests, setSOSRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardData();
    
    // Refresh every 30 seconds
    const interval = setInterval(loadDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      const [statsRes, priorityRes, alertsRes, sosRes] = await Promise.all([
        apiService.getStats(),
        apiService.getPriorityZones(),
        apiService.getCapacityAlerts(),
        apiService.getSOSRequests('PENDING')
      ]);

      setStats(statsRes.data);
      setPriorityZones(priorityRes.data.priority_zones || []);
      setShelterAlerts(alertsRes.data.alerts || []);
      setSOSRequests(sosRes.data);
      
      setError(null);
    } catch (err) {
      console.error('Failed to load dashboard:', err);
      setError('Failed to load dashboard data. Please ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  if (loading && !stats) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading Kavach AI Dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <h2>⚠️ Connection Error</h2>
        <p>{error}</p>
        <button onClick={loadDashboardData}>Retry</button>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>🚨 Kavach AI - Command Dashboard</h1>
        <div className="last-updated">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </header>

      {/* Stats Overview */}
      <section className="stats-section">
        <h2>System Overview</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">🗺️</div>
            <div className="stat-content">
              <h3>Total Zones</h3>
              <p className="stat-value">{stats?.total_zones || 0}</p>
            </div>
          </div>

          <div className="stat-card danger">
            <div className="stat-icon">🔴</div>
            <div className="stat-content">
              <h3>Red Zones</h3>
              <p className="stat-value">{stats?.red_zones || 0}</p>
            </div>
          </div>

          <div className="stat-card warning">
            <div className="stat-icon">⚠️</div>
            <div className="stat-content">
              <h3>High Priority</h3>
              <p className="stat-value">{stats?.high_priority_zones || 0}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🏥</div>
            <div className="stat-content">
              <h3>Hospitals</h3>
              <p className="stat-value">{stats?.total_hospitals || 0}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🏕️</div>
            <div className="stat-content">
              <h3>Shelters</h3>
              <p className="stat-value">{stats?.total_shelters || 0}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🏠</div>
            <div className="stat-content">
              <h3>Households</h3>
              <p className="stat-value">{stats?.total_households || 0}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Priority Zones */}
      <section className="priority-section">
        <h2>🚨 Priority Zones ({priorityZones.length})</h2>
        {priorityZones.length === 0 ? (
          <p className="no-data">No high priority zones at this time</p>
        ) : (
          <div className="priority-table">
            <table>
              <thead>
                <tr>
                  <th>Zone</th>
                  <th>Priority Score</th>
                  <th>Risk Score</th>
                  <th>Vulnerable Pop.</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {priorityZones.map((zone) => (
                  <tr key={zone.zone_id} className={zone.priority_score >= 80 ? 'critical' : ''}>
                    <td><strong>{zone.zone_name}</strong></td>
                    <td>
                      <span className="priority-badge">{zone.priority_score.toFixed(1)}</span>
                    </td>
                    <td>{zone.risk_score.toFixed(1)}</td>
                    <td>{zone.vulnerable_population}</td>
                    <td>
                      <span className="action-badge">{zone.action}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {/* Shelter Alerts */}
      {shelterAlerts.length > 0 && (
        <section className="alerts-section">
          <h2>⚠️ Shelter Capacity Alerts ({shelterAlerts.length})</h2>
          <div className="alerts-grid">
            {shelterAlerts.map((alert, index) => (
              <div key={index} className={`alert-card ${alert.status.toLowerCase()}`}>
                <div className="alert-header">
                  <h4>{alert.shelter_name}</h4>
                  <span className="alert-status">{alert.status}</span>
                </div>
                <div className="alert-body">
                  <div className="capacity-bar">
                    <div 
                      className="capacity-fill" 
                      style={{ width: `${alert.occupancy_percent}%` }}
                    ></div>
                  </div>
                  <p>Occupancy: {alert.occupancy_percent.toFixed(1)}%</p>
                  <p>Available: {alert.available_capacity} spaces</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* SOS Requests */}
      <section className="sos-section">
        <h2>🆘 Pending SOS Requests ({sosRequests.length})</h2>
        {sosRequests.length === 0 ? (
          <p className="no-data">No pending SOS requests</p>
        ) : (
          <div className="sos-grid">
            {sosRequests.slice(0, 5).map((sos) => (
              <div key={sos.id} className={`sos-card priority-${sos.priority.toLowerCase()}`}>
                <div className="sos-header">
                  <h4>{sos.emergency_type}</h4>
                  <span className="sos-priority">{sos.priority}</span>
                </div>
                <div className="sos-body">
                  <p><strong>Location:</strong> {sos.location_lat.toFixed(4)}, {sos.location_lng.toFixed(4)}</p>
                  {sos.citizen_name && <p><strong>Contact:</strong> {sos.citizen_name}</p>}
                  <p>{sos.description}</p>
                  <p className="sos-time">{new Date(sos.created_at).toLocaleString()}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Refresh Button */}
      <div className="dashboard-actions">
        <button onClick={loadDashboardData} className="refresh-btn" disabled={loading}>
          {loading ? '⟳ Refreshing...' : '🔄 Refresh Data'}
        </button>
      </div>
    </div>
  );
};

export default Dashboard;