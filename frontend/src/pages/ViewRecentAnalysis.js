import React, { useState, useEffect } from 'react';
import '../styles/Analysis-Report.css';

function ViewRecentAnalysis() {
  const [llmResponse, setLlmResponse] = useState(null);
  const [driverPlot, setDriverPlot] = useState('');
  const [userPlot, setUserPlot] = useState('');
  
  useEffect(() => {
    const storedLlmResponse = localStorage.getItem('llmResponse');
    const driverPlot = localStorage.getItem('plotUrl');
    const userPlot = localStorage.getItem('jsonPlot');

    if (storedLlmResponse) {
      setLlmResponse(storedLlmResponse);
    }

    if (driverPlot) {
      setDriverPlot(driverPlot);
    }

    if (userPlot) {
      setUserPlot(userPlot);
    }
  }, []);

  const renderLlmResponse = (response) => {
    return response.split('\n').map((line, index) => (
      <span key={index}>
        {line}
        <br />
      </span>
    ));
  };

  return (
    <div className="analysis-report-container">
      <h2 className="text-racing">View Recent Analysis</h2>

      {/* Driver Plot */}
      {driverPlot && (
        <div className="analysis-content">
          <h3>Driver Plot</h3>
          <img src={driverPlot} alt="Plot 1" className="plot-image" />
        </div>
      )}

      {/* User Plot*/}
      {userPlot && (
        <div className="analysis-content">
          <h3>User Plot</h3>
          <img src={userPlot} alt="Plot 2" className="plot-image" />
        </div>
      )}

      {/* Display LLM Response */}
      <div className="llm-response">
        <h3>LLM Analysis</h3>
        {llmResponse ? renderLlmResponse(llmResponse) : <div>No LLM Response found in local storage.</div>}
      </div>
    </div>
  );
}

export default ViewRecentAnalysis;
