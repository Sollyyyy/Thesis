import { useState, useEffect } from 'react';
import './Admin.css';
import API_BASE from '../config';

const Admin = () => {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState('');
  const [expandedUser, setExpandedUser] = useState(null);
  const [userHistory, setUserHistory] = useState([]);

  const token = localStorage.getItem('token');
  const headers = { 'Authorization': `Bearer ${token}` };

  const fetchUsers = async () => {
    try {
      const res = await fetch(`${API_BASE}/admin/users`, { headers });
      if (res.ok) {
        setUsers(await res.json());
      } else {
        const data = await res.json();
        setError(data.detail || 'Failed to load users');
      }
    } catch {
      setError('Connection error');
    }
  };

  useEffect(() => { fetchUsers(); }, []);

  const handleDelete = async (username) => {
    if (!window.confirm(`Delete user "${username}"?`)) return;
    try {
      const res = await fetch(`${API_BASE}/admin/users/${username}`, {
        method: 'DELETE', headers
      });
      if (res.ok) {
        setUsers(users.filter(u => u.username !== username));
        if (expandedUser === username) setExpandedUser(null);
      } else {
        const data = await res.json();
        alert(data.detail || 'Failed to delete user');
      }
    } catch {
      alert('Connection error');
    }
  };

  const toggleHistory = async (username) => {
    if (expandedUser === username) {
      setExpandedUser(null);
      return;
    }
    try {
      const res = await fetch(`${API_BASE}/admin/history/${username}`, { headers });
      if (res.ok) {
        setUserHistory(await res.json());
        setExpandedUser(username);
      }
    } catch {
      alert('Failed to load history');
    }
  };

  if (error) return <div className="admin-page"><div className="admin-error">{error}</div></div>;

  return (
    <div className="admin-page">
      <div className="admin-card">
        <h2>User Management</h2>
        <p className="admin-count">{users.length} registered users</p>
        <div className="users-table">
          <div className="table-header">
            <span>User</span>
            <span>Email</span>
            <span>Role</span>
            <span></span>
          </div>
          {users.map(u => (
            <div key={u.username}>
              <div className="table-row">
                <div className="user-cell">
                  <span className="user-avatar">{u.full_name.charAt(0).toUpperCase()}</span>
                  <div>
                    <span className="user-name">{u.full_name}</span>
                    <span className="user-username">@{u.username}</span>
                  </div>
                </div>
                <span className="user-email">{u.email}</span>
                <span className={`role-badge ${u.role}`}>{u.role}</span>
                <div className="row-actions">
                  <button className="history-btn" onClick={() => toggleHistory(u.username)}>
                    {expandedUser === u.username ? 'Hide' : 'History'}
                  </button>
                  {u.role !== 'admin' ? (
                    <button className="delete-btn" onClick={() => handleDelete(u.username)}>Delete</button>
                  ) : null}
                </div>
              </div>
              {expandedUser === u.username && (
                <div className="user-history">
                  {userHistory.length > 0 ? userHistory.map(h => (
                    <div key={h.id} className="history-row">
                      <span>{h.departure} → {h.destination}</span>
                      <span>{h.depart_date}</span>
                      <span className="history-date">{new Date(h.searched_at).toLocaleString()}</span>
                    </div>
                  )) : (
                    <p className="no-history">No search history</p>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Admin;
