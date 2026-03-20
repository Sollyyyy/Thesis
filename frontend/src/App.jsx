import { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import AirportSelect from './components/AirportSelect';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';

const Search = () => {
  const [departure, setDeparture] = useState('');
  const [destination, setDestination] = useState('');
  const [departDate, setDepartDate] = useState('');
  const [returnDate, setReturnDate] = useState('');
  const [results, setResults] = useState({ flight: null, bus: null, train: null });
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState('flight');

  const endpoints = {
    flight: 'http://localhost:8000/api/search',
    bus: 'http://localhost:8000/api/search/bus',
    train: 'http://localhost:8000/api/search/train',
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch(endpoints[mode], {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ departure, destination, departDate, returnDate })
      });
      const data = await response.json();
      setResults(prev => ({ ...prev, [mode]: data }));
    } catch (error) {
      console.error('Error:', error);
      setResults(prev => ({ ...prev, [mode]: { success: false, error: error.message } }));
    }
    setLoading(false);
  };

  return (
    <div className="page-content">
      <section className="hero">
        <h1>Find Your Perfect Trip</h1>
        <p>Compare flights, buses, and trains to get the best deals</p>
      </section>

      <section className="search-section">
        <div className="transport-tabs">
          <button
            className={`tab ${mode === 'flight' ? 'active' : ''}`}
            onClick={() => setMode('flight')}
            type="button"
          >
            ✈️ Flights
          </button>
          <button
            className={`tab ${mode === 'bus' ? 'active' : ''}`}
            onClick={() => setMode('bus')}
            type="button"
          >
            🚌 Buses
          </button>
          <button
            className={`tab ${mode === 'train' ? 'active' : ''}`}
            onClick={() => setMode('train')}
            type="button"
          >
            🚆 Trains
          </button>
        </div>
        <form onSubmit={handleSearch} className="search-form tabbed">
          <div className="form-row">
            <AirportSelect label="Departure" value={departure} onChange={setDeparture} />
            <AirportSelect label="Destination" value={destination} onChange={setDestination} />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Departure Date</label>
              <input
                type="date"
                value={departDate}
                onChange={(e) => setDepartDate(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Return Date</label>
              <input
                type="date"
                value={returnDate}
                onChange={(e) => setReturnDate(e.target.value)}
                required
              />
            </div>
          </div>

          <button type="submit" disabled={loading}>
            {loading ? 'Searching...' : 'Search Trips'}
          </button>
        </form>
      </section>

      {results[mode] && (
        <section className="results-section">
          <h2>{mode === 'flight' ? 'Flight' : mode === 'bus' ? 'Bus' : 'Train'} Results</h2>
          {results[mode].success === false ? (
            <div className="error">
              <p>Error: {results[mode].error}</p>
            </div>
          ) : (
            <div className="flights-list">
              {results[mode].flights && results[mode].flights.length > 0 ? (
                results[mode].flights.map((flight, index) => (
                  <div key={index} className="flight-card">
                    <div className="flight-info">
                      <h3>{flight.agent}</h3>
                      <p className="duration">⏱ {flight.duration}</p>
                    </div>
                    <p className="price">{flight.price} EUR</p>
                    <a href={flight.link} target="_blank" rel="noopener noreferrer" className="book-btn">
                      View Details
                    </a>
                  </div>
                ))
              ) : (
                <p>No results found</p>
              )}
            </div>
          )}
        </section>
      )}
    </div>
  );
};

const Layout = ({ children, isLoggedIn, onLogout, loggingOut }) => (
  <div className={`app-layout ${loggingOut ? 'fade-out' : ''}`}>
    <Navbar isLoggedIn={isLoggedIn} onLogout={onLogout} loggingOut={loggingOut} />
    <main className="main-content">{children}</main>
    <Footer />
  </div>
);

const AppRoutes = ({ isLoggedIn, handleLogin, handleLogout }) => {
  const [loggingOut, setLoggingOut] = useState(false);
  const navigate = useNavigate();

  const onLogout = () => {
    setLoggingOut(true);
    setTimeout(() => {
      handleLogout();
      setLoggingOut(false);
      navigate('/');
    }, 800);
  };

  return (
    <Layout isLoggedIn={isLoggedIn} onLogout={onLogout} loggingOut={loggingOut}>
      <Routes>
        <Route path="/login" element={
          isLoggedIn ? <Navigate to="/" /> : <Login onLogin={handleLogin} />
        } />
        <Route path="/register" element={
          isLoggedIn ? <Navigate to="/" /> : <Register />
        } />
        <Route path="/profile" element={
          isLoggedIn ? <Profile /> : <Navigate to="/login" />
        } />
        <Route path="/" element={<Search />} />
      </Routes>
    </Layout>
  );
};

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));

  const handleLogin = () => setIsLoggedIn(true);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
  };

  return (
    <BrowserRouter>
      <AppRoutes
        isLoggedIn={isLoggedIn}
        handleLogin={handleLogin}
        handleLogout={handleLogout}
      />
    </BrowserRouter>
  );
};

export default App;
