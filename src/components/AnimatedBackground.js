// src/components/AnimatedBackground.js
import React from 'react';
import '../App.css';

const AnimatedBackground = () => {
  return (
    <div className="racing-background">
      <div className="car-pulse car-1"></div>
      <div className="car-pulse car-2"></div>
      <div className="car-pulse car-3"></div>
    </div>
  );
};

export default AnimatedBackground;