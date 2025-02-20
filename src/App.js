// src/App.js
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import CompareTelemetry from './pages/CompareTelemetry';
import AnalysisReport from './pages/AnalysisReport';
import PrivateRoute from './components/PrivateRoute';
import AnimatedBackground from './components/AnimatedBackground'; 
import TrackSelection from './pages/TrackSelection';
import RaceDataEntry from './pages/RaceDataEntry';
import './App.css';

function App() {
  return (
    <Router>
      <AuthProvider>
        <AnimatedBackground /> 
        <Navigation />
        <div className="container mt-4">
          <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/select-track" element={<TrackSelection />} />
          <Route path="/enter-data/:trackId" element={<RaceDataEntry />} />
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route element={<PrivateRoute />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/compare" element={<CompareTelemetry />} />
              <Route path="/analysis/:reportId" element={<AnalysisReport />} />
            </Route>
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;