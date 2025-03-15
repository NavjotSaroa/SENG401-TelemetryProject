import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { fetchAnalysisAndPdfUnregistered, fetchAnalysisAndPdfRegistered } from '../services/api';
import '../styles/Analysis-Report.css';

function AnalysisReport() {
  const [analysis, setAnalysis] = useState('Loading analysis...');
  const [pdfUrl, setPdfUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const { state } = useLocation();
  const navigate = useNavigate();
  
  const isLoggedIn = localStorage.getItem('jwt');

  useEffect(() => {
    const fetchData = async () => {
      try {
        let data;
        if (isLoggedIn) {
          const userData = JSON.parse(localStorage.getItem('userData'));
          data = await fetchAnalysisAndPdfRegistered(userData);
        } else {
          data = await fetchAnalysisAndPdfUnregistered();
        }

        setAnalysis(data.summary_text);
        setPdfUrl(data.pdf_url);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to fetch the analysis and PDF. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [isLoggedIn]);

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
      <pre className="analysis-content">{analysis}</pre>

      {pdfUrl && (
        <div>
          <button
            className="btn btn-primary"
            onClick={() => window.open(pdfUrl, '_blank')}
          >
            Download PDF Report
          </button>
        </div>
      )}

      <button
        className="btn btn-primary"
        onClick={() => window.print()}
      >
        Export as PDF
      </button>
    </div>
  );
}

export default AnalysisReport;
