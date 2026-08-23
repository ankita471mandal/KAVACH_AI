import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Error interceptor
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const ApiService = {
  // Health & Stats
  getHealth: () => api.get('/health'),
  getStats: () => api.get('/stats'),

  // Zones
  getZones: () => api.get('/api/v1/zones/'),
  getPriorityZones: () => api.get('/api/v1/zones/priority/list'),

  // Hospitals
  getHospitals: () => api.get('/api/v1/hospitals/'),

  // Shelters
  getShelters: () => api.get('/api/v1/shelters/'),
  getShelterCapacity: (shelterId) => api.get(`/api/v1/shelters/${shelterId}/capacity`),

  // SOS
  createSOS: (data) => api.post('/api/v1/sos/', data),
  getSOSRequests: (status) => api.get(`/api/v1/sos/${status ? `?status=${status}` : ''}`),

  // Rescue
  submitRescueReport: (data) => api.post('/api/v1/rescue/report', data),

  // Roads
  getRoads: () => api.get('/api/v1/roads/'),
};

export default ApiService;