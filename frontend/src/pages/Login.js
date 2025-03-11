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

    if (!username || !password) {
      setAuthenticationMessage('All fields are required');
      return;
    }

    try {
      const response = await fetch('http://localhost:3001/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        throw new Error('Authentication failed');
      }

      const data = await response.json();

      if (data && data.token) {
        sessionStorage.setItem('jwtToken', data.token);
        setToken(data.token);
        sessionStorage.setItem('username', data.username);

        navigate(location.state?.from || '/select-track');
      } else {
        setAuthenticationMessage('Incorrect username or password');
      }
    } catch (error) {
      setAuthenticationMessage(error.message || 'An error occurred');
    }
  };

  return (
    <div className="auth-form">
      <h2 className="text-racing mb-4">Driver Login</h2>
      <form onSubmit={handleAuthentication}>
        <div className="mb-3">
          <label className="form-label">Email</label>
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
        {authenticationMessage && <p className="error-message">{authenticationMessage}</p>}
      </form>
    </div>
  );
}

export default Login;
