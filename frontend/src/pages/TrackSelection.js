import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import SeasonSelector from '../components/SeasonSelector';
import Loader from '../components/Loader';
import '../App.css';

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
          console.log("HERE from TrackSelection.js")
          setIsLoading(true);
          setError('');
          const response = await axios.get('/api/telemetry/fetch/tracklist', {
            params: { year: selectedSeason }
          });
          
          // Convert object response to array of track objects
          const tracksArray = Object.entries(response.data).map(([key, value]) => ({
            id: key,
            name: value,
            image: `/tracks/${value.toLowerCase().replace(/ /g, '-')}.jpg`
          }));
          
          setTracks(tracksArray);
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
    setSelectedTrack(null);
    setTracks([]);
  };

  const handleTrackSelect = (trackId) => {
    setSelectedTrack(trackId);
  };

  const handleContinue = () => {
    if (selectedTrack) {
      const selectedTrackData = tracks.find(track => track.id === selectedTrack);
      navigate(`/drivers/${selectedSeason}/${encodeURIComponent(selectedTrackData.name)}`);
    }
  };

  return (
    <div className="track-selection-container">
      <h1 className="text-racing mb-4">Select Season & Track</h1>
      
      <SeasonSelector 
        onSeasonSelect={handleSeasonSelect} 
        minYear={2019} 
        maxYear={2024}
      />

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
                    <div className="track-season">Season {selectedSeason}</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {selectedTrack && (
            <button 
              className="btn btn-primary mt-4"
              onClick={handleContinue}
              disabled={!selectedTrack}
            >
              Continue to Driver Selection
            </button>
          )}
        </>
      )}
    </div>
  );
};

export default TrackSelection;