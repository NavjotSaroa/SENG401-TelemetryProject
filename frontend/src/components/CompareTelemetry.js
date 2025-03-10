import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { fetchTelemetryPlot } from '../services/api'; 
import TelemetryPlot from './TelemetryPlot';

function CompareTelemetry() {
  const { year, track, driver } = useParams(); // From route params /compare/:year/:track/:driver
  const navigate = useNavigate();
  const [plotUrl, setPlotUrl] = React.useState(null);

  React.useEffect(() => {
    fetchTelemetryPlot(year, track, driver)
      .then(url => setPlotUrl(url))
      .catch(err => console.error('Error loading telemetry:', err));
  }, [year, track, driver]);

  return (
    <div className="compare-telemetry-container">
      <h2>Telemetry for {driver} - {track} {year}</h2>
      {plotUrl && <TelemetryPlot plotUrl={plotUrl} />}
      <button
  className="btn btn-primary mt-3"
  onClick={() => navigate('/enter-data', { 
    state: { 
      year, 
      track: encodeURIComponent(track), 
      driver: encodeURIComponent(driver) 
    }
  })}
>
  Enter Your Data to Compare
</button>
    </div>
  );
}

export default CompareTelemetry;