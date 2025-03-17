import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useAuthContext } from '../context/AuthContext';
import { fetchUserPlot, submitComparativeAnalysis } from '../services/api';
import '../styles/Analysis-Report.css';

function AnalysisReport() {
  const [analysis, setAnalysis] = useState('Loading analysis...');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [file, setFile] = useState(null);
  const [fileChosen, setFileChosen] = useState(false);
  const [llmResponse, setLlmResponse] = useState(null);
  const location = useLocation();

  const { token } = useAuthContext();
  const { formData, year, track, driver, theme } = location.state || {};

  console.log('Received state:', { formData, year, track, driver, theme });

  const plotUrlFromStorage = localStorage.getItem('plotUrl');

  useEffect(() => {
    setIsLoading(false);
  }, []);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setFileChosen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setError('Please upload a JSON file.');
      return;
    }

    setIsLoading(true);
    const reader = new FileReader();

    reader.onloadend = async () => {
      try {
        const fileContent = reader.result;
        const fileData = JSON.parse(fileContent);

        let imageUrl;

        if (token) {
          console.log("formData Test Analysis", formData)
          const llmResponse = await submitComparativeAnalysis(
            year,
            track,
            driver,
            formData,
            theme,
            token,
            fileData
          );
          const responsePlot = await fetchUserPlot(fileData, token);
          console.log('Response from fetchUserPlot:', responsePlot);
          console.log('Response from Comparative Analysis', llmResponse);

          setLlmResponse(llmResponse.result);
          localStorage.setItem('llmResponse', llmResponse.result);


          if (responsePlot && responsePlot.status === 200) {
            const blob = responsePlot.data;
            imageUrl = URL.createObjectURL(blob);
          } else {
            setError('Error fetching plot from the backend.');
          }
        } else {
          setError('User is not logged in.');
        }

        if (imageUrl) {
          setAnalysis(<img src={imageUrl} alt="Race Analysis Plot" className="plot-image" />);
          localStorage.setItem('jsonPlot', imageUrl);
        } else {
          setError('Failed to generate plot.');
        }
      } catch (err) {
        console.error('Error processing data:', err);
        setError('Error processing data');
      } finally {
        setIsLoading(false);
      }
    };

    reader.readAsText(file);
  };

  const renderLlmResponse = (response) => {
    return response.split('\n').map((line, index) => (
      <p key={index} style={{ whiteSpace: 'pre-line' }}>
        {line}
      </p>
    ));
  };

  if (isLoading) {
    return <div className="analysis-content">Loading...</div>;
  }

  if (error) {
    return (
      <>
        <h2 className="text-racing">Race Analysis Report</h2>
        <div className="error">{error}</div>
      </>
    );
  }

  return (
    <div className="analysis-report-container">
      <h2 className="text-racing">Race Analysis Report</h2>

      <form onSubmit={handleSubmit}>
        <input type="file" accept=".json" onChange={handleFileChange} />
        <button type="submit">Upload JSON</button>
      </form>

      <div className={`file-status ${fileChosen ? 'text-white' : ''}`}>
        {fileChosen ? <span className="filename">{file.name}</span> : 'No file chosen'}
      </div>

      {/* Plot image */}
      <div className="analysis-content">
        <h3>User Plot</h3>
        {analysis}
      </div>

      {/* Plot from localStorage */}
      {plotUrlFromStorage && (
        <div className="analysis-content">
          <h3>F1 Driver Plot</h3>
          <img src={plotUrlFromStorage} alt="Telemetry Plot" className="plot-image" />
        </div>
      )}

      {/* LLM response */}
      <div className="llm-response">
        <h3>LLM Analysis</h3>
        {llmResponse ? renderLlmResponse(llmResponse) : <div>Loading LLM response...</div>}
      </div>

      <div>
        <button className="btn btn-primary" onClick={() => window.print()}>
          Export as PDF
        </button>
      </div>
    </div>
  );
}

export default AnalysisReport;
