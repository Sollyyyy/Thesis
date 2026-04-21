import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            full_name TEXT NOT NULL,
            hashed_password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            departure TEXT NOT NULL,
            destination TEXT NOT NULL,
            depart_date TEXT NOT NULL,
            return_date TEXT,
            searched_at TEXT NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
        )
    """)
    try:
        conn.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'user'")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()


def get_user(username: str):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return dict(user) if user else None


def create_user(username: str, email: str, full_name: str, hashed_password: str, role: str = "user"):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, email, full_name, hashed_password, role) VALUES (?, ?, ?, ?, ?)",
            (username, email, full_name, hashed_password, role)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_all_users():
    conn = get_connection()
    users = conn.execute("SELECT id, username, email, full_name, role FROM users").fetchall()
    conn.close()
    return [dict(u) for u in users]


def delete_user(username: str):
    conn = get_connection()
    conn.execute("DELETE FROM search_history WHERE username = ?", (username,))
    conn.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()


def save_search(username: str, departure: str, destination: str, depart_date: str, return_date: str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO search_history (username, departure, destination, depart_date, return_date, searched_at) VALUES (?, ?, ?, ?, ?, ?)",
        (username, departure, destination, depart_date, return_date, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_search_history(username: str, limit: int = 20):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM search_history WHERE username = ? ORDER BY searched_at DESC LIMIT ?",
        (username, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
