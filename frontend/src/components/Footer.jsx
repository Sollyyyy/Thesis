import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h3>✈ Trip Planner</h3>
          <p>Find the cheapest and fastest routes across flights, buses, and trains.</p>
        </div>
        <div className="footer-section">
          <h4>Quick Links</h4>
          <a href="/">Search</a>
          <a href="/login">Login</a>
          <a href="/register">Register</a>
        </div>
        <div className="footer-section">
          <h4>Transport</h4>
          <span>Flights</span>
          <span>Buses</span>
          <span>Trains</span>
        </div>
      </div>
      <div className="footer-bottom">
        <p>&copy; {new Date().getFullYear()} Trip Planner. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
