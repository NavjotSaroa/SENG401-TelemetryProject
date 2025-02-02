// src/pages/TrackSelection.js
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';

const TrackSelection = () => {
  const [selectedTrack, setSelectedTrack] = useState(null);
  const navigate = useNavigate();

  const tracks = [
    { id: 1, name: 'Monaco Grand Prix', image: '/tracks/monaco.jpg' },
    { id: 2, name: 'Silverstone Circuit', image: '/tracks/silverstone.jpg' },
    { id: 3, name: 'Suzuka International', image: '/tracks/suzuka.jpg' },
    { id: 4, name: 'Circuit of the Americas', image: '/tracks/cota.jpg' }
  ];

  const handleTrackSelect = (trackId) => {
    setSelectedTrack(trackId);
  };

  const handleContinue = () => {
    if (selectedTrack) {
      navigate(`/enter-data/${selectedTrack}`);
    }
  };

  return (
    <div className="track-selection-container">
      <h2 className="text-racing mb-4">Select a Track</h2>
      <div className="track-grid">
        {tracks.map((track) => (
          <div 
            key={track.id}
            className={`track-card ${selectedTrack === track.id ? 'selected' : ''}`}
            onClick={() => handleTrackSelect(track.id)}
          >
            <img src={track.image} alt={track.name} className="track-image" />
            <div className="track-name">{track.name}</div>
          </div>
        ))}
      </div>
      <button 
        className="btn btn-primary mt-4"
        onClick={handleContinue}
        disabled={!selectedTrack}
      >
        Continue to Data Entry
      </button>
    </div>
  );
};

export default TrackSelection;