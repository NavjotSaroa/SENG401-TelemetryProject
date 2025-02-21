// src/components/SeasonSelector.js
import { useState, useEffect } from 'react';
import axios from 'axios';

const SeasonSelector = ({ onSeasonSelect }) => {
  const [seasons, setSeasons] = useState([]);
  const [selectedSeason, setSelectedSeason] = useState('');

  useEffect(() => {
    const fetchSeasons = async () => {
      try {
        const response = await axios.get('/api/seasons');
        setSeasons(response.data);
      } catch (error) {
        console.error('Error fetching seasons:', error);
      }
    };
    fetchSeasons();
  }, []);

  const handleSeasonChange = (e) => {
    const season = e.target.value;
    setSelectedSeason(season);
    onSeasonSelect(season);
  };

  return (
    <div className="season-selector mb-4">
      <label className="form-label">Select F1 Season:</label>
      <select 
        className="form-select"
        value={selectedSeason}
        onChange={handleSeasonChange}
      >
        <option value="">Choose a season</option>
        {seasons.map((season) => (
          <option key={season} value={season}>{season}</option>
        ))}
      </select>
    </div>
  );
};

export default SeasonSelector;