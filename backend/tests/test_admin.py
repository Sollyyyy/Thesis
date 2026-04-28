def test_admin_get_users(client, admin_header):
    res = client.get("/api/admin/users", headers=admin_header)
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_admin_get_users_forbidden(client, auth_header):
    res = client.get("/api/admin/users", headers=auth_header)
    assert res.status_code == 403


def test_admin_get_users_no_auth(client):
    res = client.get("/api/admin/users")
    assert res.status_code == 401


def test_admin_delete_user(client, admin_header, test_user):
    res = client.delete(f"/api/admin/users/{test_user['username']}", headers=admin_header)
    assert res.status_code == 200
    assert "deleted" in res.json()["message"]


def test_admin_delete_self(client, admin_header, admin_user):
    res = client.delete(f"/api/admin/users/{admin_user['username']}", headers=admin_header)
    assert res.status_code == 400


def test_admin_delete_nonexistent(client, admin_header):
    res = client.delete("/api/admin/users/nobody", headers=admin_header)
    assert res.status_code == 404


def test_regular_user_cannot_delete(client, auth_header, admin_user):
    res = client.delete(f"/api/admin/users/{admin_user['username']}", headers=auth_header)
    assert res.status_code == 403
