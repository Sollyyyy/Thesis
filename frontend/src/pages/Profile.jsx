import { useState, useEffect } from 'react';
import './Profile.css';

const Profile = () => {
  const [user, setUser] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/api/profile', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
          const data = await response.json();
          setUser(data);
        } else {
          setError('Failed to load profile');
        }
      } catch (err) {
        setError('Connection error');
      }
    };
    fetchProfile();
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
          <p className="coming-soon">Coming soon...</p>
        </div>
      </div>
    </div>
  );
};

export default Profile;
