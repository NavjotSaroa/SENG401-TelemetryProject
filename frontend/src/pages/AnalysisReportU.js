import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { submitSingleAnalysis } from '../services/api';
import '../styles/Analysis-Report.css';

function AnalysisReportU() {
  const [analysis, setAnalysis] = useState('Loading analysis...');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [hasFetched, setHasFetched] = useState(false);
  const location = useLocation();

  const { track, year, driver, theme } = location.state || {};

  const plotUrl = localStorage.getItem('plotUrl');

  useEffect(() => {
    if (hasFetched) return;

    const fetchAnalysis = async () => {
      if (!track || !year || !driver || !theme) {
        setError('Missing track or data.');
        return;
      }

      setIsLoading(true);

      try {
        const analysisResult = await submitSingleAnalysis(year, track, driver, theme);

        if (analysisResult && analysisResult.result) {
          setAnalysis(analysisResult.result); 
        } else {
          setError('Failed to fetch analysis.');
        }
      } catch (err) {
        console.error('Error fetching analysis:', err);
        setError('Error fetching analysis.');
      } finally {
        setIsLoading(false);
        setHasFetched(true);
      }
    };

    fetchAnalysis();
  }, [track, year, driver, theme, hasFetched]);

  const formatAnalysis = (text) => {
    return text.split('-').map((line, index) => (
      <p key={index}>{line.trim()}</p>
    ));
  };

  if (isLoading) {
    return <div className="analysis-content">Loading analysis...</div>;
  }

  if (error) {
    return (
      <div className="analysis-report-container">
        <h2 className="text-racing">Race Analysis Report</h2>
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div className="analysis-report-container">
      <h2 className="text-racing">Race Analysis Report</h2>

      {/* Plot URL from localStorage */}
      {plotUrl && (
        <div className="analysis-content">
          <h3>Analysis Plot</h3>
          <img src={plotUrl} alt="Analysis Plot" className="plot-image" />
        </div>
      )}
      <br />

      {/* LLM */}
      <div className="analysis-content">
        <h3>Analysis Result:</h3>
        <div>{formatAnalysis(analysis)}</div>
      </div>
      <br />

      <div>
        <button className="btn btn-primary" onClick={() => window.print()}>
          Export as PDF
        </button>
      </div>
    </div>
  );
}

export default AnalysisReportU;
