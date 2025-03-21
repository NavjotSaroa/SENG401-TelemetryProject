import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuthContext } from '../context/AuthContext';

function RaceDataEntry() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const { year, track, driver } = state || {};

  const { token } = useAuthContext();
  const isAuthenticated = Boolean(token);

  const [formData, setFormData] = useState({
    onThrottleDiff: '',
    frontCamber: '',
    rearCamber: '',
    frontSuspension: '',
    rearSuspension: '',
    frontWingAero: '',
    rearWingAero: '',
  });
  const [theme, setTheme] = useState('default');
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
      navigate('/analysisR/report-id', {
        state: {
          formData, 
          year, 
          track, 
          driver, 
          theme,
        },
      });
    } catch (err) {
      setError('Failed to proceed to the next page. Please check your input and try again.');
      console.error('Error submitting data:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="race-data-entry-container">
      <h2>Enter Your Racing Data for {track} {year}</h2>
      <p>Comparing with driver #{driver}</p>
      <form className="auth-form" onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">On Throttle Differential Percentage (50 to 100):</label>
          <input
            type="text"
            name="onThrottleDiff"
            value={formData.onThrottleDiff}
            onChange={handleChange}
            className="form-control"
            min="50"
            max="100"
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Front Camber (-3.50 to -2.50):</label>
          <input
            type="number"
            name="frontCamber"
            value={formData.frontCamber}
            onChange={handleChange}
            className="form-control"
            min="-3.50"
            max="-2.50"
            step="0.01"
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Rear Camber (-2.00 to -1.00):</label>
          <input
            type="text"
            name="rearCamber"
            value={formData.rearCamber}
            onChange={handleChange}
            className="form-control"
            min="-2.00"
            max="-1.00"
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Front Suspension (1 to 41):</label>
          <input
            type="text"
            name="frontSuspension"
            value={formData.frontSuspension}
            onChange={handleChange}
            className="form-control"
            min="1"
            max="41"
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Rear Suspension (1 to 41):</label>
          <input
            type="text"
            name="rearSuspension"
            value={formData.rearSuspension}
            onChange={handleChange}
            className="form-control"
            min="1"
            max="41"
            required
          />
        </div>
        {isAuthenticated && (
          <>
            <div className="mb-3">
              <label className="form-label">Front Wing Aero (0 to 50):</label>
              <input
                type="number"
                name="frontWingAero"
                value={formData.frontWingAero}
                onChange={handleChange}
                className="form-control"
                min="0"
                max="50"
                required
              />
            </div>
            <div className="mb-3">
              <label className="form-label">Rear Wing Aero (0 to 50):</label>
              <input
                type="number"
                name="rearWingAero"
                value={formData.rearWingAero}
                onChange={handleChange}
                className="form-control"
                min="0"
                max="50"
                required
              />
            </div>
          </>
        )}
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
