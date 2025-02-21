// src/services/api.js
import axios from 'axios';

const API_BASE = 'http://localhost:3000/api/telemetry'; // Flask server URL

export const fetchTracks = async (year) => {
    try {
      const response = await axios.get(`${API_BASE}/fetch/tracklist`, {
        params: { year }
      });
      return Object.values(response.data); // Convert object to array
    } catch (error) {
      console.error('Error fetching tracks:', error);
      throw error;
    }
  };
  
  export const fetchDrivers = async (year, track) => {
    try {
      const response = await axios.get(`${API_BASE}/fetch/drivers`, {
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
      const response = await axios.get(`${API_BASE}/fetch/telemetry`, {
        params: { year, track, driver },
        responseType: 'blob' // for binary image data
      });
      return URL.createObjectURL(new Blob([response.data]));
    } catch (error) {
      console.error('Error fetching telemetry:', error);
      throw error;
    }
  };
  