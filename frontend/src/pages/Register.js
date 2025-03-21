import { useState } from 'react';
import '../styles/Login-Registration.css';
import Login from './Login';

const Register = () => {
  const [userData, setUserData] = useState({
    username: '',
    password: '',
    confirmPassword: ''
  });

  const [registrationMessage, setRegistrationMessage] = useState('');
  const [showLogin, setShowLogin] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setRegistrationMessage('');

    const { username, password, confirmPassword } = userData;

    if (!username || !password || !confirmPassword) {
      setRegistrationMessage('All fields are required');
      setIsLoading(false);
      return;
    }

    if (password !== confirmPassword) {
      setRegistrationMessage('Passwords do not match');
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch('https://seng401-telemetryproject-d3hw.onrender.com/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          username: username,
          password: password
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Registration failed. Please try again.');
      }

      setRegistrationMessage('Registration successful! Redirecting to login...');
      setTimeout(() => setShowLogin(true), 2000);

    } catch (error) {
      console.error('Registration error:', error);
      setRegistrationMessage(
        error.message || 'An error occurred during registration. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  if (showLogin) {
    return <Login />;
  }

  return (
    <div className="auth-form">
      <h2 className="text-racing mb-4">Create Racing Account</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Username (Email)</label>
          <input
            type="email"
            className="form-control"
            value={userData.username}
            onChange={(e) => setUserData({ ...userData, username: e.target.value })}
            required
          />
        </div>
        
        <div className="mb-3">
          <label className="form-label">Password</label>
          <input
            type="password"
            className="form-control"
            value={userData.password}
            onChange={(e) => setUserData({ ...userData, password: e.target.value })}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Confirm Password</label>
          <input
            type="password"
            className="form-control"
            value={userData.confirmPassword}
            onChange={(e) => setUserData({ ...userData, confirmPassword: e.target.value })}
            required
          />
        </div>

        <button 
          type="submit" 
          className="btn btn-primary w-100"
          disabled={isLoading}
        >
          {isLoading ? 'Registering...' : 'Register'}
        </button>

        {registrationMessage && (
          <div className={`mt-3 alert ${registrationMessage.includes('successful') ? 'alert-success' : 'alert-danger'}`}>
            {registrationMessage}
          </div>
        )}
      </form>
    </div>
  );
};

export default Register;