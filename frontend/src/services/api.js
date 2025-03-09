// src/services/api.js
import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:3001/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Credentials': true
  }
});
// Base URLs for different API groups
const TELEMETRY_BASE = 'http://localhost:3001/api/telemetry';
const AUTH_BASE = 'http://localhost:3001/api/auth';           

API.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});


export const fetchDrivers = async (year, track) => {
  try {
    const response = await axios.get(`${TELEMETRY_BASE}/fetch/drivers`, {
      params: { year, track }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching drivers:', error);
    throw error;
  }
};

export const fetchTelemetryPlot = async (year, track, driver) => {
  try {
    const response = await axios.get(`${TELEMETRY_BASE}/fetch/telemetry`, {
      params: { year, track, driver },
      responseType: 'blob' // for binary image data
    });
    return URL.createObjectURL(new Blob([response.data]));
  } catch (error) {
    console.error('Error fetching telemetry:', error);
    throw error;
  }
};


export const loginUser = async (username, password) => {
  try {
    const response = await axios.post(`${AUTH_BASE}/login`, {
      username,
      password
    });
    return response.data; 
  } catch (error) {
    console.error('Error logging in:', error.response?.data || error.message);
    throw error;
  }
};
