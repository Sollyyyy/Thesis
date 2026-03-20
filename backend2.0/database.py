import sqlite3
import os

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
            hashed_password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_user(username: str):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return dict(user) if user else None


def create_user(username: str, email: str, full_name: str, hashed_password: str):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, email, full_name, hashed_password) VALUES (?, ?, ?, ?)",
            (username, email, full_name, hashed_password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
