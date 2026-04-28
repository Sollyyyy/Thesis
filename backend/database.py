import pymysql
import time
from datetime import datetime
from config import (MYSQL_HOST, MYSQL_PORT, MYSQL_USER,
                    MYSQL_PASSWORD, MYSQL_DATABASE)


def get_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )


def init_db():
    # Retry connection until MySQL is ready
    for attempt in range(30):
        try:
            conn = get_connection()
            break
        except Exception:
            print(f"Waiting for MySQL... (attempt {attempt + 1})")
            time.sleep(2)
    else:
        raise Exception("Could not connect to MySQL after 30 attempts")

    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255) NOT NULL,
            full_name VARCHAR(255) NOT NULL,
            hashed_password TEXT NOT NULL,
            role VARCHAR(50) NOT NULL DEFAULT 'user'
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            departure VARCHAR(255) NOT NULL,
            destination VARCHAR(255) NOT NULL,
            depart_date VARCHAR(50) NOT NULL,
            searched_at VARCHAR(50) NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()


def get_user(username: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    conn.close()
    return user


def create_user(username: str, email: str, full_name: str,
                hashed_password: str, role: str = "user"):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, email, full_name,"
            " hashed_password, role) VALUES (%s, %s, %s, %s, %s)",
            (username, email, full_name, hashed_password, role)
        )
        conn.commit()
        return True
    except pymysql.IntegrityError:
        return False
    finally:
        conn.close()


def get_all_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email, full_name, role FROM users")
    users = cur.fetchall()
    conn.close()
    return users


def delete_user(username: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM search_history WHERE username = %s", (username,))
    cur.execute("DELETE FROM users WHERE username = %s", (username,))
    conn.commit()
    conn.close()


def save_search(username: str, departure: str, destination: str,
                depart_date: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO search_history (username, departure, destination,"
        " depart_date, searched_at) "
        "VALUES (%s, %s, %s, %s, %s)",
        (username, departure, destination, depart_date,
         datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_search_history(username: str, limit: int = 20):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM search_history WHERE username = %s"
        " ORDER BY searched_at DESC LIMIT %s",
        (username, limit)
    )
    rows = cur.fetchall()
    conn.close()
    return rows
