// src/pages/DriverSelection.js
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchDrivers } from '../services/api';
import '../App.css';

const DriverSelection = () => {
  const { year, track } = useParams();
  const [drivers, setDrivers] = useState([]);
  const [selectedDriver, setSelectedDriver] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const loadDrivers = async () => {
      try {
        setLoading(true);
        const driversData = await fetchDrivers(year, track);
        const mappedDrivers = Object.entries(driversData).map(([number, name]) => ({
          number,
          name
        }));
        setDrivers(mappedDrivers);
      } catch (error) {
        console.error('Error loading drivers:', error);
        setError('Failed to load drivers. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    loadDrivers();
  }, [year, track]);

  const handleCompare = () => {
    if (selectedDriver) {
      localStorage.setItem('selectedDriver', selectedDriver);
      navigate(`/compare/${year}/${track}/${selectedDriver}`);
    }
  };

  return (
    <div className="driver-selection-page">
      <div className="overlay"></div>
      <div className="driver-selection-container">
        <h2 className="text-racing">Select Driver - {track} {year}</h2>
        {loading ? (
          <div className="loader-container">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          </div>
        ) : error ? (
          <p className="alert alert-danger">{error}</p>
        ) : (
          <>
            <select 
              value={selectedDriver}
              onChange={(e) => setSelectedDriver(e.target.value)}
              className="form-select driver-select"
            >
              <option value="">Select Driver</option>
              {drivers.map(driver => (
                <option key={driver.number} value={driver.number}>
                  {driver.name} (#{driver.number})
                </option>
              ))}
            </select>
            <button onClick={handleCompare} disabled={!selectedDriver} className="btn btn-primary mt-3">
              Show Telemetry
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default DriverSelection;
