import { useState, useRef, useEffect } from 'react';
import airports from '../airports';

const AirportSelect = ({ value, onChange, label }) => {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const ref = useRef(null);

  const filtered = airports.filter((a) =>
    `${a.code} ${a.name} ${a.city} ${a.country}`.toLowerCase().includes(query.toLowerCase())
  );

  const selected = airports.find((a) => a.code === (value?.code || value));

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setIsOpen(false);
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="form-group" ref={ref}>
      <label>{label}</label>
      <div className="airport-select">
        <input
          type="text"
          value={isOpen ? query : selected ? `${selected.code} - ${selected.city}` : ''}
          onChange={(e) => { setQuery(e.target.value); setIsOpen(true); }}
          onFocus={() => { setIsOpen(true); setQuery(''); }}
          placeholder="Search airport..."
          required
        />
        {isOpen && (
          <ul className="airport-dropdown">
            {filtered.length > 0 ? (
              filtered.map((a) => (
                <li
                  key={a.code}
                  className={a.code === value?.code ? 'selected' : ''}
                  onClick={() => { onChange({ code: a.code, city: a.city }); setIsOpen(false); setQuery(''); }}
                >
                  <span className="airport-code">{a.code}</span>
                  <span className="airport-detail">{a.city} - {a.name} ({a.country})</span>
                </li>
              ))
            ) : (
              <li className="no-results">No airports found</li>
            )}
          </ul>
        )}
      </div>
    </div>
  );
};

export default AirportSelect;
