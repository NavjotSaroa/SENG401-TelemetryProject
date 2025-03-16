import React, { useState, useEffect } from 'react';
import { useAuthContext } from '../context/AuthContext';
import { fetchUserPlot } from '../services/api';
import '../styles/Analysis-Report.css';

// import { fetchAnalysisAndPdfUnregistered, fetchAnalysisAndPdfRegistered } from '../services/api';


function AnalysisReport() {
  const [analysis, setAnalysis] = useState('Loading analysis...');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [file, setFile] = useState(null);
  const [fileChosen, setFileChosen] = useState(false);

  const { token } = useAuthContext();

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
          const response = await fetchUserPlot(fileData, token);
          console.log('Response from fetchUserPlot:', response);
  
          if (response && response.status === 200) {
            const blob = response.data; 
            imageUrl = URL.createObjectURL(blob);
          } else {
            setError('Error fetching plot from the backend.');
          }
        } else {
          setError('User is not logged in.');
        }
  
        if (imageUrl) {
          setAnalysis(<img src={imageUrl} alt="Race Analysis Plot" className="plot-image" />);
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
        <input
          type="file"
          accept=".json"
          onChange={handleFileChange}
        />
        <button type="submit">Upload JSON</button>
      </form>

      <div className={`file-status ${fileChosen ? 'text-white' : ''}`}>
        {fileChosen ? (
          <span className="filename">{file.name}</span>
        ) : (
          'No file chosen'
        )}
      </div>

      {/* Display the plot image once it has been fetched */}
      <div className="analysis-content">
        {analysis}
      </div>

      <div>
        <button
          className="btn btn-primary"
          onClick={() => window.print()}
        >
          Export as PDF
        </button>
      </div>
    </div>
  );
}

export default AnalysisReport;
