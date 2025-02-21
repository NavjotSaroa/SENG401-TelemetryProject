const TelemetryPlot = ({ plotUrl }) => {
    return (
      <div className="mt-4 racing-plot">
        <img 
          src={plotUrl} 
          alt="Telemetry Comparison" 
          className="img-fluid"
          style={{ maxHeight: '600px', border: '2px solid #FF1801' }}
        />
      </div>
    );
  };
  
  export default TelemetryPlot;