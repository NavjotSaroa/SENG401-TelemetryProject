import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import TelemetryPlot from '../components/TelemetryPlot';

const AnalysisReport = () => {
  const { reportId } = useParams();
  const [report, setReport] = useState(null);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const res = await axios.get(`/api/reports/${reportId}`);
        setReport(res.data);
      } catch (error) {
        console.error('Failed to load report:', error);
      }
    };
    fetchReport();
  }, [reportId]);

  return (
    <div className="analysis-report">
      {report ? (
        <>
          <h2 className="text-racing">{report.title}</h2>
          <div className="report-content">
            <TelemetryPlot plotUrl={report.plotUrl} />
            <div className="analysis-text mt-4 p-3">
              <h4>AI Analysis</h4>
              <p>{report.analysis}</p>
              <div className="btn-group">
                <a
                  href={report.pdfUrl}
                  className="btn btn-primary"
                  download
                >
                  Download PDF
                </a>
                <a
                  href={report.imageUrl}
                  className="btn btn-success"
                  download
                >
                  Download Image
                </a>
              </div>
            </div>
          </div>
        </>
      ) : (
        <p>Loading report...</p>
      )}
    </div>
  );
};

export default AnalysisReport;