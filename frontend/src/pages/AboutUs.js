import React from 'react';
import '../App.css';

function AboutUs() {
  const members = [
    { name: "Oussama Ouadihi", emoji: "🧙" },
    { name: "Navjot Saroa", emoji: "🧮" },
    { name: "Ernesto Barreto", emoji: "🤖" },
    { name: "Jaimal Sahota", emoji: "🛰️" }
  ];

  return (
    <div className="aboutus-container">
      <div className="dynamic-grid">
        {Array(16).fill().map((_, i) => (
          <div key={i} className="grid-particle" style={{ '--delay': i * 0.1 }}></div>
        ))}
      </div>

      <h2 className="cyber-title">
        <span className="glitch-text">SOFTWARE ENGINEERING</span>
        <br/>
        <span className="glitch-text">TEAM</span>
      </h2>

      <div className="member-grid">
        {members.map((member, index) => (
          <div key={index} className="member-card">
            <div className="emoji-halo">{member.emoji}</div>
            <div className="name-plate">
              <span className="member-number">0{index + 1}</span>
              {member.name}
            </div>
          </div>
        ))}
      </div>

      <div className="team-statement">
        <p>
          Third-year software engineering student at the University of Calgary<br/>
          Converging diverse technical interests to pioneer<br/>
          next-generation AI powered telemetry analysis systems
        </p>
      </div>
    </div>
  );
}

export default AboutUs;