// src/pages/CompareTelemetry.js
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchTelemetryPlot } from '../services/api';

const CompareTelemetry = () => {
  const { year, track, driver } = useParams();
  const [plotUrl, setPlotUrl] = useState('');

  useEffect(() => {
    const loadTelemetry = async () => {
      try {
        const url = await fetchTelemetryPlot(year, track, driver);
        setPlotUrl(url);
      } catch (error) {
        // Handle error
      }
    };
    loadTelemetry();
  }, [year, track, driver]);

  return (
    <div className="telemetry-comparison">
      <h2>Telemetry for {driver} - {track} {year}</h2>
      {plotUrl && <img src={plotUrl} alt="Telemetry Plot" />}
    </div>
  );
};
export default CompareTelemetry;