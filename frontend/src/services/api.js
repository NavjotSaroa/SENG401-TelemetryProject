// src/services/api.js
import axios from 'axios';

// Base URLs for different API groups
const TELEMETRY_BASE = 'http://localhost:3000/api/telemetry';
const AUTH_BASE = 'http://localhost:3000/api/auth';           

export const fetchTracks = async (year) => {
  try {
    const response = await axios.get(`${TELEMETRY_BASE}/fetch/tracklist`, {
      params: { year }
    });
    return Object.values(response.data); 
  } catch (error) {
    console.error('Error fetching tracks:', error);
    throw error;
  }
};

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
