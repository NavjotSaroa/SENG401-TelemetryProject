import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import SeasonSelector from '../components/SeasonSelector';
import Loader from '../components/Loader'; 

const TrackSelection = () => {
  const [selectedTrack, setSelectedTrack] = useState(null);
  const [tracks, setTracks] = useState([]);
  const [selectedSeason, setSelectedSeason] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTracks = async () => {
      if (selectedSeason) {
        try {
          setIsLoading(true);
          setError('');
          const response = await axios.get(`/api/tracks/${selectedSeason}`);
          setTracks(response.data);
        } catch (err) {
          setError('Failed to load tracks. Please try again later.');
          console.error('Error fetching tracks:', err);
        } finally {
          setIsLoading(false);
        }
      }
    };

    fetchTracks();
  }, [selectedSeason]);

  const handleSeasonSelect = (season) => {
    setSelectedSeason(season);
    setSelectedTrack(null); // Reset track selection on season change
  };

  const handleTrackSelect = (trackId) => {
    setSelectedTrack(trackId);
  };

  const handleContinue = () => {
    if (selectedTrack) {
      navigate(`/enter-data/${selectedSeason}/${selectedTrack}`);
    }
  };

  return (
    <div className="track-selection-container">
      <h1 className="text-racing mb-4">Select Season & Track</h1>
      
      <SeasonSelector onSeasonSelect={handleSeasonSelect} />

      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}

      {isLoading ? (
        <Loader />
      ) : (
        <>
          {selectedSeason && (
            <div className="track-grid">
              {tracks.map((track) => (
                <div
                  key={track.id}
                  className={`track-card ${selectedTrack === track.id ? 'selected' : ''}`}
                  onClick={() => handleTrackSelect(track.id)}
                >
                  <img 
                    src={track.image} 
                    alt={track.name} 
                    className="track-image" 
                    onError={(e) => {
                      e.target.src = '/tracks/default-track.jpg';
                    }}
                  />
                  <div className="track-info">
                    <div className="track-name">{track.name}</div>
                    <div className="track-location">
                      <span className="flag-icon">{track.countryFlag}</span>
                      {track.location}
                    </div>
                    <div className="track-date">
                      {new Date(track.date).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {selectedTrack && (
            <button 
              className="btn btn-primary mt-4"
              onClick={handleContinue}
            >
              Continue to Data Entry
            </button>
          )}
        </>
      )}
    </div>
  );
};

export default TrackSelection;