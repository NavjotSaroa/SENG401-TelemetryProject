// src/pages/DriverSelection.js
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchDrivers } from '../services/api';

const DriverSelection = () => {
  const { year, track } = useParams();
  const [drivers, setDrivers] = useState([]);
  const [selectedDriver, setSelectedDriver] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const loadDrivers = async () => {
      try {
        const driversData = await fetchDrivers(year, track);
        setDrivers(Object.entries(driversData).map(([number, name]) => ({
          number,
          name
        })));
      } catch (error) {
        // Handle error
      }
    };
    loadDrivers();
  }, [year, track]);

  const handleCompare = () => {
    navigate(`/compare/${year}/${track}/${selectedDriver}`);
  };

  return (
    <div className="driver-selection">
      <h2>Select Driver - {track} {year}</h2>
      <select 
        value={selectedDriver}
        onChange={(e) => setSelectedDriver(e.target.value)}
      >
        <option value="">Select Driver</option>
        {drivers.map(driver => (
          <option key={driver.number} value={driver.number}>
            {driver.name} (#{driver.number})
          </option>
        ))}
      </select>
      <button onClick={handleCompare} disabled={!selectedDriver}>
        Show Telemetry
      </button>
    </div>
  );
};
export default DriverSelection