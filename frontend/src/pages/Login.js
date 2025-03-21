import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuthContext } from '../context/AuthContext';
import '../styles/Login-Registration.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [authenticationMessage, setAuthenticationMessage] = useState('');
  const { setToken } = useAuthContext();
  const navigate = useNavigate();
  const location = useLocation();

  const handleAuthentication = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch('https://seng401-telemetryproject-d3hw.onrender.com/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Authentication failed');
      }

      if (data.token) {
        sessionStorage.setItem('jwtToken', data.token);
        setToken(data.token);
        sessionStorage.setItem('username', data.username);
        navigate(location.state?.from || '/select-track');
      }
    } catch (error) {
      console.error('Login error:', error);
      setAuthenticationMessage(error.message || 'Invalid credentials. Please try again.');
    }
  };

  return (
    <div className="auth-form">
      <h2 className="text-racing mb-4">Driver Login</h2>
      <form onSubmit={handleAuthentication}>
        <div className="mb-3">
          <label className="form-label">Username</label>
          <input
            type="text"
            className="form-control"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Password</label>
          <input
            type="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary w-100">
          Sign In
        </button>
        {authenticationMessage && (
          <div className="mt-3 alert alert-danger">
            {authenticationMessage}
          </div>
        )}
      </form>
    </div>
  );
}

export default Login;