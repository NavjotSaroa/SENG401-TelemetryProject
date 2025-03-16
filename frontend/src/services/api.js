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

export const fetchTelemetryPlot = async (year, track, driver, theme) => {
  try {
    const response = await axios.get(`${TELEMETRY_BASE}/fetch/telemetry`, {
      params: { year, track, driver, theme },
      responseType: 'blob' // for binary image data
    });
    return URL.createObjectURL(new Blob([response.data]));
  } catch (error) {
    console.error('Error fetching telemetry:', error.response?.data || error.message);
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


export const fetchAnalysisAndPdfUnregistered = async () => {
  try {
    const response = await axios.get(`${TELEMETRY_BASE}/fetch/unregistered_LLM_and_pdf`);
    return response.data;
  } catch (error) {
    console.error('Error fetching unregistered analysis and PDF:', error);
    throw error;
  }
};

export const fetchAnalysisAndPdfRegistered = async (userData) => {
  try {
    const response = await axios.get(`${TELEMETRY_BASE}/fetch/registered_LLM_and_pdf`, {
      params: {
        user_data: JSON.stringify(userData),
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching registered analysis and PDF:', error);
    throw error;
  }
};

export const fetchUserPlot = async (fileData, token) => {
  const year = localStorage.getItem('selectedYear');
  const theme = localStorage.getItem('selectedTheme');
  const driver = localStorage.getItem('selectedDriver');
  const track = localStorage.getItem('selectedTrack');
  const userDataStr = JSON.stringify(fileData);

  const url = `${TELEMETRY_BASE}/fetch/registered_telemetry?user_data=${userDataStr}&year=${year}&track=${track}&driver=${driver}&theme=${theme}`;

  try {
    const response = await axios.get(url, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      responseType: 'blob',
    });

    return response;
  } catch (err) {
    console.error('Error in fetchUserPlot:', err);
    throw err;
  }
};
