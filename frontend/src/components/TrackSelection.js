import React, { useState } from 'react';

const TrackSelection = () => {
    const [season, setSeason] = useState('');
    const [tracks, setTracks] = useState([]);
    const [error, setError] = useState('');
  
    useEffect(() => {
      if (season) {
        fetchTracks(season);
      }
    }, [season]);
  
    const fetchTracks = async (season) => {
      try {
        const response = await fetch(`/api/telemetry/fetch/tracklist?year=${season}`);
        if (!response.ok) {
          throw new Error('Failed to fetch track list');
        }
        const data = await response.json();
        setTracks(Object.values(data));
      } catch (err) {
        setError(err.message);
      }
    };

  return (
    <div className="track-selection-container">
      <h2>Select a Season</h2>
      <select value={season} onChange={handleSeasonChange}>
        <option value="">-- Choose a Season --</option>
        <option value="2019">2019</option>
        <option value="2020">2020</option>
        <option value="2021">2021</option>
        <option value="2022">2022</option>
        <option value="2023">2023</option>
        <option value="2024">2024</option>
      </select>
      {error && <p className="alert alert-danger">{error}</p>}
      <div className="track-grid">
        {tracks.length > 0 ? (
          tracks.map((track, index) => (
            <div key={index} className="track-card">
              <div className="track-info">
                <h5 className="track-name">{track}</h5>
              </div>
            </div>
          ))
        ) : (
          season && <p>No tracks found for this season.</p>
        )}
      </div>
    </div>
  );
};

export default TrackSelection;
