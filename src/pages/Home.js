import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css'; 

const Home = () => {
  return (
    <div className="home-container">
      {/* Video Background */}
      <div className="video-container">
        <video autoPlay loop muted playsInline className="background-video">
          <source src="/f1-race.mp4" type="video/mp4" />
          Your browser does not support HTML5 video.
        </video>
        <div className="video-overlay"></div>
      </div>

      {/* Content */}
      <div className="home-content">
        <h1 className="display-4 text-racing mb-4">BonoGPT</h1>
        <p className="lead">Compare your racing performance with professional F1 drivers</p>
        <div className="mt-5">
        <Link to="/select-track" className="btn btn-primary btn-lg me-3">
          Get Started
        </Link>
        
          <Link to="/compare" className="btn btn-outline-light btn-lg">
            Login
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Home;