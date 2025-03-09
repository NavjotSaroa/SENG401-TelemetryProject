import React from 'react';
import { useLocation } from 'react-router-dom';

function AnalysisReport() {
  const { state } = useLocation();
  const analysis = state?.analysis || 'No analysis available.';

  return (
    <div className="analysis-report-container">
      <h2>Race Analysis Report</h2>
      <pre className="analysis-content">{analysis}</pre>
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