import { Link, NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { GiRaceCar } from 'react-icons/gi';

const Navigation = () => {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <Link className="navbar-brand" to="/">
          <GiRaceCar className="me-2" />
          BonoGPT
        </Link>
        <div className="collapse navbar-collapse">
          <ul className="navbar-nav me-auto">
            <li className="nav-item">
              <NavLink className="nav-link" to="/">Home</NavLink>
            </li>
            {user && (
              <>
                <li className="nav-item">
                  <NavLink className="nav-link" to="/dashboard">Dashboard</NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className="nav-link" to="/compare">Compare</NavLink>
                </li>
              </>
            )}
          </ul>
          <div className="d-flex">
            {user ? (
              <button className="btn btn-outline-light" onClick={logout}>
                Logout
              </button>
            ) : (
              <>
                <Link to="/login" className="btn btn-outline-light me-2">
                  Login
                </Link>
                <Link to="/register" className="btn btn-primary">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;