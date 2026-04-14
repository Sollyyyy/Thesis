import { useState, useEffect } from 'react';
import './Profile.css';
import API_BASE from '../config';

const Profile = () => {
  const [user, setUser] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');

  const token = localStorage.getItem('token');
  const headers = { 'Authorization': `Bearer ${token}` };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [profileRes, historyRes] = await Promise.all([
          fetch(`${API_BASE}/profile`, { headers }),
          fetch(`${API_BASE}/history`, { headers })
        ]);
        if (profileRes.ok) setUser(await profileRes.json());
        else setError('Failed to load profile');
        if (historyRes.ok) setHistory(await historyRes.json());
      } catch {
        setError('Connection error');
      }
    };
    fetchData();
  }, []);

  if (error) return <div className="profile-page"><div className="profile-error">{error}</div></div>;
  if (!user) return <div className="profile-page"><p className="profile-loading">Loading...</p></div>;

  return (
    <div className="profile-page">
      <div className="profile-card">
        <div className="profile-avatar">{user.full_name.charAt(0).toUpperCase()}</div>
        <h2>{user.full_name}</h2>
        <div className="profile-details">
          <div className="profile-field">
            <span className="profile-label">Username</span>
            <span className="profile-value">{user.username}</span>
          </div>
          <div className="profile-field">
            <span className="profile-label">Email</span>
            <span className="profile-value">{user.email}</span>
          </div>
        </div>
        <div className="profile-section">
          <h3>Search History</h3>
          {history.length > 0 ? (
            <div className="history-list">
              {history.map((h) => (
                <div key={h.id} className="history-item">
                  <div className="history-route">
                    <span className="history-city">{h.departure}</span>
                    <span className="history-arrow">→</span>
                    <span className="history-city">{h.destination}</span>
                  </div>
                  <div className="history-meta">
                    <span>{h.depart_date}{h.return_date ? ` — ${h.return_date}` : ''}</span>
                    <span className="history-time">{new Date(h.searched_at).toLocaleDateString()}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="coming-soon">No searches yet</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile;
