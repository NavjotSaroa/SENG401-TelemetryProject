import { useState } from 'react';
import axios from 'axios';
import TelemetryPlot from '../components/TelemetryPlot';

const CompareTelemetry = () => {
  const [selectedDriver, setSelectedDriver] = useState('');
  const [comparisonId, setComparisonId] = useState(null);
  const [plotUrl, setPlotUrl] = useState('');
  const [analysis, setAnalysis] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('telemetry', file);
    
    try {
      await axios.post('/api/telemetry/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };

  const handleCompare = async () => {
    setIsLoading(true);
    try {
      const res = await axios.post('/api/compare', {
        driverId: selectedDriver
      });
      setComparisonId(res.data.comparisonId);
      setPlotUrl(`/api/plots/${res.data.comparisonId}`);
    } catch (error) {
      console.error('Comparison failed:', error);
    }
    setIsLoading(false);
  };

  const generateAnalysis = async () => {
    try {
      const res = await axios.post('/api/analysis', { comparisonId });
      setAnalysis(res.data.analysis);
    } catch (error) {
      console.error('Analysis failed:', error);
    }
  };

  return (
    <div className="telemetry-comparison">
      <h2 className="text-racing">Compare Telemetry</h2>
      
      <div className="mb-3">
        <select 
          className="form-select"
          value={selectedDriver}
          onChange={(e) => setSelectedDriver(e.target.value)}
        >
          <option value="">Select F1 Driver</option>
          {/* Populate from backend API */}
        </select>
      </div>

      <div className="mb-3">
        <label className="form-label">
          Upload Your Telemetry File (CSV/JSON)
        </label>
        <input 
          type="file" 
          className="form-control"
          accept=".json,.csv"
          onChange={handleFileUpload}
        />
      </div>

      <button 
        className="btn btn-primary"
        onClick={handleCompare}
        disabled={!selectedDriver || isLoading}
      >
        {isLoading ? 'Comparing...' : 'Compare Data'}
      </button>

      {plotUrl && (
        <>
          <TelemetryPlot plotUrl={plotUrl} />
          <button 
            className="btn btn-success mt-3"
            onClick={generateAnalysis}
          >
            Generate AI Analysis
          </button>
        </>
      )}

      {analysis && (
        <div className="analysis-result mt-4 p-3">
          <h4>AI Analysis</h4>
          <p>{analysis}</p>
          <div className="btn-group">
            <a 
              href={`/api/export/pdf?analysis=${encodeURIComponent(analysis)}`}
              className="btn btn-secondary"
              target="_blank"
              rel="noreferrer"
            >
              Download PDF
            </a>
            <a 
              href={`/api/export/image?analysis=${encodeURIComponent(analysis)}`}
              className="btn btn-secondary"
              target="_blank"
              rel="noreferrer"
            >
              Download Image
            </a>
          </div>
        </div>
      )}
    </div>
  );
};

export default CompareTelemetry;