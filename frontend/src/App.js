import { AuthProvider } from './context/AuthContext';
import Navigation from './components/Navigation';
import AnimatedBackground from './components/AnimatedBackground';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import CompareTelemetry from './components/CompareTelemetry';
import AnalysisReport from './pages/AnalysisReport';
import TrackSelection from './pages/TrackSelection';
import RaceDataEntry from './components/RaceDataEntry';
import DriverSelection from './pages/DriverSelection';  
import ViewRecentAnalysis from './pages/ViewRecentAnalysis';
import AboutUs from './pages/AboutUs';

import './App.css';
import { BrowserRouter as Router, Route, Routes, Navigate, useLocation } from 'react-router-dom';

function AppRoutes() {
  const location = useLocation();
  const isDriverSelection = location.pathname.startsWith('/drivers/');

  return (
    <>
      <AnimatedBackground />
      <Navigation />
      {/* Only wrap in .container.mt-4 if it's NOT the Driver Selection page */}
      {!isDriverSelection ? (
        <div className="container mt-4">
          <RoutesContent />
        </div>
      ) : (
        <RoutesContent />
      )}
    </>
  );
}

function RoutesContent() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/select-track" element={<TrackSelection />} />
      <Route path="/enter-data/:trackId" element={<RaceDataEntry />} />
      <Route path="/enter-data" element={<RaceDataEntry />} />

      <Route path="/view-recent" element={<ViewRecentAnalysis />} />
      <Route path="/about-us" element={<AboutUs />} />
      
      {/* Driver Selection Route (Fullscreen Background) */}
      <Route path="/drivers/:year/:track" element={<DriverSelection />} />
      <Route path="/compare/:year/:track/:driver" element={<CompareTelemetry />} />
      <Route path="/analysis/:reportId" element={<AnalysisReport />} />

      {/* Redirects */}
      <Route path="/get-started" element={<Navigate to="/select-track" />} />

      {/* 404 Fallback */}
      <Route path="*" element={<h1 className="text-racing">404 - Page Not Found</h1>} />
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </Router>
  );
}

export default App;
