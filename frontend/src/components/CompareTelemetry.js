// src/pages/CompareTelemetry.js
import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchTelemetryPlot } from '../services/api';
import TelemetryPlot from '../components/TelemetryPlot';
import '../App.css';

const CompareTelemetry = () => {
  // Extract URL parameters for year, track, and driver
  const { year, track, driver } = useParams();
  const navigate = useNavigate();

  const [theme, setTheme] = useState('default');
  const [plotUrl, setPlotUrl] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Fetch the telemetry plot with the selected theme
  const handleShowTelemetry = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const url = await fetchTelemetryPlot(year, track, driver, theme);
      localStorage.setItem('selectedTheme', theme);
      localStorage.setItem('plotUrl', url); 
      setPlotUrl(url);
    } catch (err) {
      console.error('Error fetching telemetry plot:', err);
      setError('Failed to load telemetry plot. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  // Proceed to data entry page, passing state (year, track, driver)
  const proceedToNextPage = () => {
    const token = sessionStorage.getItem('jwtToken');
    if (token) {
      navigate('/enter-data', { state: { year, track, driver } });
    } 
    else {
      navigate('/analysisU/report-id', {
        state: {plotUrl, year, track, driver, theme} });
    }
  };

  return (
    <div className="compare-telemetry-container">
      <h2 className="text-racing">
        Telemetry for {track} ({year}) - Driver: {driver}
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
            <option value="barbie">Barbie</option>
            
          </select>
        </div>
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Loading...' : 'Show Telemetry'}
        </button>
      </form>
      {error && <p className="alert alert-danger mt-3">{error}</p>}
      {plotUrl && (
        <div className="mt-4">
          <TelemetryPlot plotUrl={plotUrl} />
          {/* Button to proceed to data entry page */}
          <button onClick={proceedToNextPage} className="btn btn-secondary mt-3">
            Proceed to Analysis
          </button>
        </div>
      )}
    </div>
  );
};

export default CompareTelemetry;
