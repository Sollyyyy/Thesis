import { useState, useEffect } from 'react';
import './Admin.css';

const Admin = () => {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState('');

  const token = localStorage.getItem('token');
  const headers = { 'Authorization': `Bearer ${token}` };

  const fetchUsers = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/admin/users', { headers });
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
      const res = await fetch(`http://localhost:8000/api/admin/users/${username}`, {
        method: 'DELETE', headers
      });
      if (res.ok) {
        setUsers(users.filter(u => u.username !== username));
      } else {
        const data = await res.json();
        alert(data.detail || 'Failed to delete user');
      }
    } catch {
      alert('Connection error');
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
            <div key={u.username} className="table-row">
              <div className="user-cell">
                <span className="user-avatar">{u.full_name.charAt(0).toUpperCase()}</span>
                <div>
                  <span className="user-name">{u.full_name}</span>
                  <span className="user-username">@{u.username}</span>
                </div>
              </div>
              <span className="user-email">{u.email}</span>
              <span className={`role-badge ${u.role}`}>{u.role}</span>
              {u.role !== 'admin' ? (
                <button className="delete-btn" onClick={() => handleDelete(u.username)}>Delete</button>
              ) : (
                <span className="delete-placeholder"></span>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Admin;
