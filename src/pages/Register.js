import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const [userData, setUserData] = useState({
    username: '',
    email: '',
    password: ''
  });
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    await register(userData);
    navigate('/dashboard');
  };

  return (
    <div className="auth-form">
      <h2 className="text-racing mb-4">Create Racing Account</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Username</label>
          <input
            type="text"
            className="form-control"
            value={userData.username}
            onChange={(e) => setUserData({...userData, username: e.target.value})}
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Email</label>
          <input
            type="email"
            className="form-control"
            value={userData.email}
            onChange={(e) => setUserData({...userData, email: e.target.value})}
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Password</label>
          <input
            type="password"
            className="form-control"
            value={userData.password}
            onChange={(e) => setUserData({...userData, password: e.target.value})}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary w-100">
          Register
        </button>
      </form>
    </div>
  );
};

export default Register;