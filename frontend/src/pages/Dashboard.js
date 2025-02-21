import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();

  return (
    <div className="dashboard">
      <h2 className="text-racing">Welcome, {user?.username}</h2>
      <div className="mt-4">
        <Link to="/compare" className="btn btn-primary me-3">
          New Comparison
        </Link>
        <Link to="/analysis/recent" className="btn btn-outline-light">
          View Recent Analysis
        </Link>
      </div>
    </div>
  );
};

export default Dashboard;