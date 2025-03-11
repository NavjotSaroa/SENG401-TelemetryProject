// src/pages/CompareTelemetry.js

import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import { fetchTelemetryPlot } from '../services/api';
import '../App.css';

const CompareTelemetry = () => {
  // Expect URL: /compare/:year/:track/:driver
  const { year, track, driver } = useParams();
  const [theme, setTheme] = useState('default'); 
  const [plotUrl, setPlotUrl] = useState([]);
  
  const [error, setError] = useState('');

  useEffect(() => {
    fetch("/themes.json")
      .then((response) => response.json())
      .then((data) => setTheme(Object.entries(data)))
      .catch((err) => console.error("Error loading themes:", err));
  }, []);

  const handleShowTelemetry = async (e) => {
    e.preventDefault();
    setError('');
    try {
      // Call the API 
      const url = await fetchTelemetryPlot(year, track, driver, theme);
      setPlotUrl(url);
    } catch (err) {
      console.error("Error fetching telemetry plot:", err);
      setError("Failed to load telemetry plot. Please try again later.");
    }
  };

  return (
    <div className="compare-telemetry-container">
      <h2 className="text-racing">
        Telemetry for {track} {year} - Driver: {driver}
      </h2>
      <form onSubmit={handleShowTelemetry}>
        <div className="mb-3">
          <label className="form-label">Select Plot Theme:</label>
          <select
            className="form-select"
            value={theme}
            onChange={(e) => setTheme(e.target.value)}
            required
          >
            <option value="default">Default</option>
            <option value="cyberpunk">Cyberpunk</option>
            <option value="barbie">barbie</option>
          
          </select>
        </div>
        <button type="submit" className="btn btn-primary">
          Show Telemetry
        </button>
      </form>
      {error && <p className="alert alert-danger mt-3">{error}</p>}
      {plotUrl && (
        <div className="mt-4">
          <img src={plotUrl} alt="Telemetry Plot" style={{ maxWidth: '100%' }} />
        </div>
      )}
    </div>
  );
};

export default CompareTelemetry;
