import React, { useState, useEffect } from 'react';
import { useAuthContext } from '../context/AuthContext';
import { fetchUserPlot } from '../services/api';
import '../styles/Analysis-Report.css';

// import { fetchAnalysisAndPdfUnregistered, fetchAnalysisAndPdfRegistered } from '../services/api';

function ViewRecentAnalysis() {
  const [analysis, setAnalysis] = useState('Loading analysis...');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [file, setFile] = useState(null);
  const [fileChosen, setFileChosen] = useState(false);

  const { token } = useAuthContext();

  return (
    <div className="analysis-report-container">
      <h2 className="text-racing">View Recent Analysis</h2>

    </div>
  );
}

export default ViewRecentAnalysis;
