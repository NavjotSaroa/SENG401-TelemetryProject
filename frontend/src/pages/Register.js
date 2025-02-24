import { useState } from 'react';
import '../styles/Login-Registration.css';
import Login from './Login';

const Register = () => {
  const [userData, setUserData] = useState({
    username: '',
    password: '',
  });

  const [registrationMessage, setRegistrationMessage] = useState('');
  const [showLogin, setShowLogin] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const { username, password} = userData;

    if (!username || !password) {
      setRegistrationMessage('All fields are required');
      return;
    }

    if (!/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/.test(username)) {
      setRegistrationMessage('Please enter a valid username address');
      return;
    }

    const registrationRequest = {
      credentials: {
        username,
        password
      }
    };

    try {
      const registrationResponse = await fetch('http://localhost:8080/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(registrationRequest),
      });

      if (!registrationResponse.ok) {
        throw new Error('Registration failed Try again');
      }

      const registrationData = await registrationResponse.json();

      await fetch(`http://localhost:8080/user/${registrationData.user}/update-details`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(registrationData),
      });

      setRegistrationMessage('Registration successful');
      setShowLogin(true);

    } catch (error) {
      console.error('Error registering:', error);
      setRegistrationMessage(error.message || 'An error occurred during registration');
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
          <label className="form-label">Email</label>
          <input
            type="username"
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
        <button type="submit" className="btn btn-primary w-100">
          Register
        </button>
        {registrationMessage && <p className="error-message">{registrationMessage}</p>}
      </form>
    </div>
  );
};

export default Register;
