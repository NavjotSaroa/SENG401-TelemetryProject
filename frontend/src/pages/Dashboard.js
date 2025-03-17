import { Link } from 'react-router-dom';
import { useAuthContext } from '../context/AuthContext';

const Dashboard = () => {
  const { user } = useAuthContext();

  return (
    <div className="dashboard">
      <h2 className="text-racing">Welcome, {user?.username}</h2>
      <div className="mt-4">
        <Link to="/select-track" className="btn btn-primary me-3">
          New Comparison
        </Link>
        <Link to="/view-recent" className="btn btn-outline-light">
          View Recent Analysis
        </Link>
      </div>
    </div>
  );
};

export default Dashboard;