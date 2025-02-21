import { AuthProvider } from './context/AuthContext';
import Navigation from './components/Navigation';
import AnimatedBackground from './components/AnimatedBackground';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import CompareTelemetry from './pages/CompareTelemetry';
import AnalysisReport from './pages/AnalysisReport';
import TrackSelection from './pages/TrackSelection';
import RaceDataEntry from './pages/RaceDataEntry';
import './App.css';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';

function App() {
  return (
    <Router>
      <AuthProvider>
        <AnimatedBackground />
        <Navigation />
        <div className="container mt-4">
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/select-track" element={<TrackSelection />} />
            <Route path="/enter-data/:trackId" element={<RaceDataEntry />} />
            <Route path="/compare/:year/:track/:driver" element={<CompareTelemetry />} />
            <Route path="/analysis/:reportId" element={<AnalysisReport />} />

            {/* Redirects */}
            <Route path="/get-started" element={<Navigate to="/select-track" />} />

            {/* 404 Fallback */}
            <Route path="*" element={<h1 className="text-racing">404 - Page Not Found</h1>} />
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
