import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h3>Trip Planner</h3>
          <p>Find the cheapest and fastest routes across flights, buses, and trains.</p>
        </div>
        <div className="footer-section">
          <h4>Quick Links</h4>
          <a href="/">Search</a>
          <a href="/login">Login</a>
          <a href="/register">Register</a>
        </div>
        <div className="footer-section">
          <h4>Contact Us</h4>
          <a href="mailto:zeyadsoliman@gmail.com">Email us</a>
          <a href="tel:555-555-5555">Call us</a>
        </div>
      </div>
      <div className="footer-bottom">
        <p>&copy; 2026 Trip Planner. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
