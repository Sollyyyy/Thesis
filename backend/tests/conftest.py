import pytest
from fastapi.testclient import TestClient
from argon2 import PasswordHasher
from main import app
from database import init_db, get_connection, create_user

ph = PasswordHasher()


@pytest.fixture(autouse=True)
def setup_db():
    """Ensure tables exist before each test."""
    init_db()
    yield
    # Cleanup test users after each test
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM search_history WHERE username LIKE 'test%'")
    cur.execute("DELETE FROM users WHERE username LIKE 'test%'")
    conn.commit()
    conn.close()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_user():
    """Create a test user and return credentials."""
    username = "testuser"
    password = "testpass123"
    create_user(username, "test@test.com", "Test User", ph.hash(password))
    return {"username": username, "password": password}


@pytest.fixture
def admin_user():
    """Create a test admin user and return credentials."""
    username = "testadmin"
    password = "adminpass123"
    create_user(username, "admin@test.com", "Test Admin", ph.hash(password), "admin")
    return {"username": username, "password": password}


@pytest.fixture
def auth_header(client, test_user):
    """Get auth header for a regular user."""
    res = client.post("/api/login", json=test_user)
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_header(client, admin_user):
    """Get auth header for an admin user."""
    res = client.post("/api/login", json=admin_user)
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
