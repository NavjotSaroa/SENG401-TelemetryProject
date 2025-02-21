// src/pages/RaceDataEntry.js
import { useParams } from 'react-router-dom';
import { useState } from 'react';
import '../App.css';

const RaceDataEntry = () => {
  const { trackId } = useParams();
  const [formData, setFormData] = useState({
    lapTime: '',
    topSpeed: '',
    sector1: '',
    sector2: '',
    sector3: ''
  });

  const tracks = {
    1: 'Monaco Grand Prix',
    2: 'Silverstone Circuit',
    3: 'Suzuka International',
    4: 'Circuit of the Americas'
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // submission logic here to be added later
    console.log('Submitted data:', { trackId, ...formData });
  };

  return (
    <div className="data-entry-container">
      <h2 className="text-racing mb-4">Enter Race Data for {tracks[trackId]}</h2>
      <form onSubmit={handleSubmit}>
        <div className="row g-3">
          <div className="col-md-6">
            <label className="form-label">Best Lap Time (mm:ss:ms)</label>
            <input
              type="text"
              className="form-control"
              pattern="\d{2}:\d{2}:\d{3}"
              placeholder="00:00:000"
              value={formData.lapTime}
              onChange={(e) => setFormData({...formData, lapTime: e.target.value})}
              required
            />
          </div>
          <div className="col-md-6">
            <label className="form-label">Top Speed (km/h)</label>
            <input
              type="number"
              className="form-control"
              min="100"
              max="400"
              value={formData.topSpeed}
              onChange={(e) => setFormData({...formData, topSpeed: e.target.value})}
              required
            />
          </div>
          <div className="col-md-4">
            <label className="form-label">Sector 1 Time</label>
            <input
              type="text"
              className="form-control"
              pattern="\d{2}:\d{2}:\d{3}"
              placeholder="00:00:000"
              value={formData.sector1}
              onChange={(e) => setFormData({...formData, sector1: e.target.value})}
              required
            />
          </div>
          <div className="col-md-4">
            <label className="form-label">Sector 2 Time</label>
            <input
              type="text"
              className="form-control"
              pattern="\d{2}:\d{2}:\d{3}"
              placeholder="00:00:000"
              value={formData.sector2}
              onChange={(e) => setFormData({...formData, sector2: e.target.value})}
              required
            />
          </div>
          <div className="col-md-4">
            <label className="form-label">Sector 3 Time</label>
            <input
              type="text"
              className="form-control"
              pattern="\d{2}:\d{2}:\d{3}"
              placeholder="00:00:000"
              value={formData.sector3}
              onChange={(e) => setFormData({...formData, sector3: e.target.value})}
              required
            />
          </div>
        </div>
        <button type="submit" className="btn btn-primary mt-4">
          Submit Race Data
        </button>
      </form>
    </div>
  );
};

export default RaceDataEntry;