import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Error handling interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Health & Stats
  getHealth: () => api.get('/health'),
  getStats: () => api.get('/stats'),

  // Zones
  getZones: () => api.get('/zones/'),
  getZone: (id) => api.get(`/zones/${id}`),
  getPriorityZones: () => api.get('/zones/priority/list'),

  // Hazards
  getHazards: () => api.get('/hazards/'),
  createHazard: (data) => api.post('/hazards/', data),
  predictRiskML: (data) => api.post('/hazards/ml-predict', data),

  // Hospitals
  getHospitals: () => api.get('/hospitals/'),
  getHospital: (id) => api.get(`/hospitals/${id}`),

  // Shelters
  getShelters: () => api.get('/shelters/'),
  getShelterCapacity: (id) => api.get(`/shelters/${id}/capacity`),
  allocateEvacuees: (zoneId, count) => 
    api.post(`/shelters/allocate?zone_id=${zoneId}&evacuee_count=${count}`),
  getCapacityAlerts: () => api.get('/shelters/alerts'),

  // Households
  getHouseholds: (zoneId = null) => {
    const url = zoneId ? `/households/?zone_id=${zoneId}` : '/households/';
    return api.get(url);
  },
  getHouseholdVulnerability: (id) => api.get(`/households/${id}/vulnerability`),

  // Roads
  getRoads: () => api.get('/roads/'),
  updateRoadStatus: (roadId, status, updatedBy) =>
    api.put(`/roads/${roadId}/status?status=${status}&updated_by=${updatedBy}`),

  // SOS
  getSOSRequests: (status = null) => {
    const url = status ? `/sos/?status=${status}` : '/sos/';
    return api.get(url);
  },
  createSOS: (data) => api.post('/sos/', data),

  // Rescue
  submitRescueReport: (data) => api.post('/rescue/report', data),
  getRescueReports: () => api.get('/rescue/reports'),
};

export default apiService;