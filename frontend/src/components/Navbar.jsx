import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = ({ isLoggedIn, isAdmin, onLogout, loggingOut }) => {
  return (
    <nav className="navbar">
      <div className="nav-content">
        <Link to="/" className="nav-logo">✈ Trip Planner</Link>
        <div className="nav-links">
          <Link to="/" className="nav-item">Search</Link>
          {isLoggedIn ? (
            <>
              {isAdmin && <Link to="/admin" className="nav-item nav-admin">Admin</Link>}
              <Link to="/profile" className="nav-item">Profile</Link>
              <button className="nav-logout" onClick={onLogout} disabled={loggingOut}>
                {loggingOut ? 'Logging out...' : 'Logout'}
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-item">Login</Link>
              <Link to="/register" className="nav-btn">Sign Up</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
