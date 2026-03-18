import { useState } from 'react';
import './App.css';
import AirportSelect from './components/AirportSelect';

const App = () => {
  const [departure, setDeparture] = useState('');
  const [destination, setDestination] = useState('');
  const [departDate, setDepartDate] = useState('');
  const [returnDate, setReturnDate] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResults(null);
    try {
      const response = await fetch('http://localhost:8000/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ departure, destination, departDate, returnDate })
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error:', error);
      setResults({ success: false, error: error.message });
    }
    setLoading(false);
  };

  return (
    <div className="app">
      <div className="container">
        <h1>Trip Planner</h1>
        <p className="subtitle">Find the cheapest and fastest routes</p>
        
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

        {results && (
          <div className="results">
            <h2>Flight Results</h2>
            {results.success === false ? (
              <div className="error">
                <p>Error: {results.error}</p>
              </div>
            ) : (
              <div className="flights-list">
                {results.flights && results.flights.length > 0 ? (
                  results.flights.map((flight, index) => (
                    <div key={index} className="flight-card">
                      <div className="flight-info">
                        <h3>{flight.agent}</h3>
                        <p className="price">{flight.price} EUR</p>
                      </div>
                      <a href={flight.link} target="_blank" rel="noopener noreferrer" className="book-btn">
                        View Details
                      </a>
                    </div>
                  ))
                ) : (
                  <p>No flights found</p>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default App;