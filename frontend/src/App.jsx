import { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import AirportSelect from './components/AirportSelect';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import Admin from './pages/Admin';

const Search = () => {
  const [departure, setDeparture] = useState(null);
  const [destination, setDestination] = useState(null);
  const [departDate, setDepartDate] = useState('');
  const [returnDate, setReturnDate] = useState('');
  const [results, setResults] = useState({ flight: null, bus: null, train: null });
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState('flight');
  const [sortBy, setSortBy] = useState('cheapest');
  const [directOnly, setDirectOnly] = useState(false);

  const getFilteredItems = () => {
    const data = results[mode];
    if (!data || !data.items) return [];
    let items = [...data.items];

    if (directOnly) {
      items = items.filter(i => (i.transfers ?? 0) === 0);
    }

    if (sortBy === 'cheapest') {
      items.sort((a, b) => (a.price || 9999) - (b.price || 9999));
    } else if (sortBy === 'fastest') {
      const parseDur = (d) => {
        if (!d || d === 'N/A') return 9999;
        const h = parseInt(d.match(/(\d+)h/)?.[1] || '0');
        const m = parseInt(d.match(/(\d+)m/)?.[1] || '0');
        return h * 60 + m;
      };
      items.sort((a, b) => parseDur(a.duration) - parseDur(b.duration));
    }

    return items;
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    if (!departure || !destination) return setLoading(false);
    try {
      const response = await fetch('http://localhost:8000/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          departure: departure.code,
          departureCity: departure.city,
          destination: destination.code,
          destinationCity: destination.city,
          departDate,
          returnDate
        })
      });
      const data = await response.json();
      // Normalize items for each mode
      const normalize = (d) => {
        if (!d || !d.success) return d;
        return { ...d, items: d.flights || d.trips || [] };
      };
      setResults({
        flight: normalize(data.flight),
        bus: normalize(data.bus),
        train: normalize(data.train)
      });
    } catch (error) {
      console.error('Error:', error);
      const err = { success: false, error: error.message };
      setResults({ flight: err, bus: err, train: err });
    }
    setLoading(false);
  };

  const today = new Date().toISOString().split('T')[0];

  return (
    <div className="page-content">
      <section className="hero">
        <h1>Find Your Perfect Trip</h1>
        <p>Compare flights, buses, and trains to get the best deals</p>
      </section>

      <section className="search-section">
        <form onSubmit={handleSearch} className="search-form">
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
                onChange={(e) => {
                  setDepartDate(e.target.value);
                  if (returnDate && e.target.value > returnDate) setReturnDate('');
                }}
                min={today}
                required
              />
            </div>
            <div className="form-group">
              <label>Return Date</label>
              <input
                type="date"
                value={returnDate}
                onChange={(e) => setReturnDate(e.target.value)}
                min={departDate || today}
                required
              />
            </div>
          </div>

          <button type="submit" disabled={loading}>
            {loading ? 'Searching...' : 'Search Trips'}
          </button>
        </form>
      </section>

      {results.flight && (
        <>
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

          {results[mode] && (
            <section className="results-section">
              <h2>{mode === 'flight' ? 'Flight' : mode === 'bus' ? 'Bus' : 'Train'} Results</h2>
              <div className="filter-bar">
                <div className="sort-buttons">
                  <button type="button" className={`filter-btn ${sortBy === 'cheapest' ? 'active' : ''}`} onClick={() => setSortBy('cheapest')}>💰 Cheapest</button>
                  <button type="button" className={`filter-btn ${sortBy === 'fastest' ? 'active' : ''}`} onClick={() => setSortBy('fastest')}>⚡ Fastest</button>
                </div>
                <button type="button" className={`filter-btn ${directOnly ? 'active' : ''}`} onClick={() => setDirectOnly(!directOnly)}>Direct only</button>
              </div>
              {results[mode].success === false ? (
                <div className="error">
                  <p>Error: {results[mode].error}</p>
                </div>
              ) : (
                <div className="flights-list">
                  {getFilteredItems().length > 0 ? (
                    getFilteredItems().map((item, index) => (
                      <div key={index} className="flight-card">
                        <div className="flight-info">
                          <h3>
                            {mode === 'flight' ? item.agent :
                             mode === 'bus' ? item.provider :
                             (item.trains || []).join(' → ') || 'Train'}
                          </h3>
                          {mode === 'bus' && item.departure_station && (
                            <p className="stations">
                              {item.departure_station} ({new Date(item.departure).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})})
                              {' → '}
                              {item.arrival_station} ({new Date(item.arrival).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})})
                            </p>
                          )}
                          {mode === 'train' && item.origin && (
                            <p className="stations">
                              {item.origin} ({new Date(item.departure).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})})
                              {' → '}
                              {item.destination} ({new Date(item.arrival).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})})
                            </p>
                          )}
                          <p className="duration">⏱ {item.duration}</p>
                          {item.transfers !== undefined && (
                            <p className="transfers">
                              {item.transfers === 0 ? 'Direct' : `${item.transfers} transfer${item.transfers > 1 ? 's' : ''}`}
                            </p>
                          )}
                        </div>
                        <p className="price">{item.price ? `${item.price} ${item.currency || 'EUR'}` : ''}</p>
                        <div className="card-right">
                          {(mode === 'bus' || mode === 'train') && item.departure && (
                            <span className="time-info">
                              {new Date(item.departure).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                              {' → '}
                              {item.arrival && new Date(item.arrival).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                            </span>
                          )}
                          <a href={item.link} target="_blank" rel="noopener noreferrer" className="book-btn">
                            View Details
                          </a>
                        </div>
                      </div>
                    ))
                  ) : (
                    <p>No results found</p>
                  )}
                </div>
              )}
            </section>
          )}
        </>
      )}
    </div>
  );
};

const Layout = ({ children, isLoggedIn, isAdmin, onLogout, loggingOut }) => (
  <div className={`app-layout ${loggingOut ? 'fade-out' : ''}`}>
    <Navbar isLoggedIn={isLoggedIn} isAdmin={isAdmin} onLogout={onLogout} loggingOut={loggingOut} />
    <main className="main-content">{children}</main>
    <Footer />
  </div>
);

const AppRoutes = ({ isLoggedIn, isAdmin, handleLogin, handleLogout }) => {
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
    <Layout isLoggedIn={isLoggedIn} isAdmin={isAdmin} onLogout={onLogout} loggingOut={loggingOut}>
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
        <Route path="/admin" element={
          isAdmin ? <Admin /> : <Navigate to="/" />
        } />
        <Route path="/" element={<Search />} />
      </Routes>
    </Layout>
  );
};

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));

  const getRole = () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return 'user';
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.role || 'user';
    } catch { return 'user'; }
  };

  const isAdmin = isLoggedIn && getRole() === 'admin';

  const handleLogin = () => setIsLoggedIn(true);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
  };

  return (
    <BrowserRouter>
      <AppRoutes
        isLoggedIn={isLoggedIn}
        isAdmin={isAdmin}
        handleLogin={handleLogin}
        handleLogout={handleLogout}
      />
    </BrowserRouter>
  );
};

export default App;
