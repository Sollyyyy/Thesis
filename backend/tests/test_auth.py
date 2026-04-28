def test_register_success(client):
    res = client.post("/api/register", json={
        "username": "testnew",
        "email": "new@test.com",
        "full_name": "New User",
        "password": "password123"
    })
    assert res.status_code == 200
    assert res.json()["message"] == "User registered successfully"


def test_register_duplicate(client, test_user):
    res = client.post("/api/register", json={
        "username": test_user["username"],
        "email": "dup@test.com",
        "full_name": "Dup User",
        "password": "password123"
    })
    assert res.status_code == 400
    assert "already exists" in res.json()["detail"]


def test_login_success(client, test_user):
    res = client.post("/api/login", json=test_user)
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_wrong_password(client, test_user):
    res = client.post("/api/login", json={
        "username": test_user["username"],
        "password": "wrongpassword"
    })
    assert res.status_code == 401


def test_login_nonexistent_user(client):
    res = client.post("/api/login", json={
        "username": "nobody",
        "password": "password123"
    })
    assert res.status_code == 401


def test_profile_authenticated(client, auth_header):
    res = client.get("/api/profile", headers=auth_header)
    assert res.status_code == 200
    assert res.json()["username"] == "testuser"
    assert res.json()["role"] == "user"


def test_profile_no_token(client):
    res = client.get("/api/profile")
    assert res.status_code == 401


def test_profile_invalid_token(client):
    res = client.get("/api/profile", headers={"Authorization": "Bearer invalidtoken"})
    assert res.status_code == 401
