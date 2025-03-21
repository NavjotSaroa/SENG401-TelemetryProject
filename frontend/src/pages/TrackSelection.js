// src/pages/TrackSelection.js
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import SeasonSelector from '../components/SeasonSelector';
import Loader from '../components/Loader';
import '../App.css';
import API from '../services/api';
console.log("API import:", API);

const TrackSelection = () => {
  const [selectedSeason, setSelectedSeason] = useState('');
  const [tracks, setTracks] = useState([]);
  const [selectedTrack, setSelectedTrack] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTracks = async () => {
      if (selectedSeason) {
        try {
          setIsLoading(true);
          setError('');
          const response = await API.get('/telemetry/fetch/tracklist', {
            params: { year: selectedSeason }
          });
          
          const tracksArray = Object.values(response.data);
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
    localStorage.setItem('selectedYear', season);
  };

  const handleTrackSelect = (trackName) => {
    setSelectedTrack(trackName);
    localStorage.setItem('selectedTrack', trackName);
  };

  const handleContinue = () => {
    if (selectedTrack) {
      navigate(`/drivers/${selectedSeason}/${encodeURIComponent(selectedTrack)}`);
    }
  };

  return (
    <div className="track-selection-page">
      {/* Video Background */}
      <div className="video-container">
        <video autoPlay loop muted playsInline className="background-video">
          <source src="/f1-race.mp4" type="video/mp4" />
          Your browser does not support HTML5 video.
        </video>
        <div className="video-overlay"></div>
      </div>

      {/* Main Content */}
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
            {selectedSeason && tracks.length > 0 && (
              <div className="track-list">
                <ul className="list-group">
                  {tracks.map((track, index) => (
                    <li 
                      key={index} 
                      className={`list-group-item track-item ${selectedTrack === track ? 'selected' : ''}`}
                      onClick={() => handleTrackSelect(track)}
                    >
                      <span className="track-name">{track}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {selectedSeason && !isLoading && tracks.length === 0 && !error && (
              <p>No tracks found for this season.</p>
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
    </div>
  );
};

export default TrackSelection;
