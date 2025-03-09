// src/components/RaceDataEntry.js
import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';

function RaceDataEntry() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const { year, track, driver } = state || {}; // Passed from CompareTelemetry

  const [formData, setFormData] = useState({
    lapTime: '',
    topSpeed: '',
    sector1: '',
    sector2: '',
    sector3: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:3001/api/report_gen/comparative-analysis', {
        year,
        track,
        driver,
        user_data: formData,
      }, {
        withCredentials: true,
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      navigate('/analysis', { state: { analysis: response.data.result } });
    } catch (err) {
      setError('Failed to generate analysis. Please check your input and try again.');
      console.error('Error submitting data:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="race-data-entry-container">
      <h2>Enter Your Racing Data for {track} {year}</h2>
      <p>Comparing with {driver}</p>
      <form className="auth-form" onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Lap Time (e.g., 1:23.456):</label>
          <input
            type="text"
            name="lapTime"
            value={formData.lapTime}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Top Speed (km/h):</label>
          <input
            type="number"
            name="topSpeed"
            value={formData.topSpeed}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Sector 1 Time (e.g., 0:28.123):</label>
          <input
            type="text"
            name="sector1"
            value={formData.sector1}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Sector 2 Time (e.g., 0:27.890):</label>
          <input
            type="text"
            name="sector2"
            value={formData.sector2}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Sector 3 Time (e.g., 0:27.543):</label>
          <input
            type="text"
            name="sector3"
            value={formData.sector3}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        {loading && <p>Loading...</p>}
        {error && <p className="alert alert-danger">{error}</p>}
        <button type="submit" className="btn btn-primary" disabled={loading}>
          Submit for Analysis
        </button>
      </form>
    </div>
  );
}

export default RaceDataEntry;