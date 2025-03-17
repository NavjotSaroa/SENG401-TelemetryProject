import { Link, NavLink } from 'react-router-dom';
import { useAuthContext } from '../context/AuthContext';
import { GiRaceCar } from 'react-icons/gi';

const Navigation = () => {
  const { token, logout } = useAuthContext();

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <Link className="navbar-brand" to="/">
        <GiRaceCar className="me-2" />
        BonoGPT
      </Link>
      <div className="collapse navbar-collapse">
        <ul className="navbar-nav me-auto">
          <li className="nav-item">
            <NavLink className="nav-link" to="/">Home</NavLink>
          </li>

          {/* If token exists, show protected routes */}
          {token && (
            <>
              <li className="nav-item">
                <NavLink className="nav-link" to="/dashboard">Dashboard</NavLink>
              </li>
            </>
          )}

          <li className="nav-item">
            <NavLink className="nav-link" to="/about-us">About Us</NavLink>
          </li>
        </ul>

        <div className="d-flex">
          {/* If token exists, show Logout button */}
          {token ? (
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
    </nav>
  );
};

export default Navigation;