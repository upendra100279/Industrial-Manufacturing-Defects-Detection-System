"""
Tests for registration, login, and protected /auth/me access.
"""
def test_register_user(client):
    res = client.post("/api/auth/register", json={
        "username": "testuser1",
        "email": "testuser1@example.com",
        "password": "SecurePass123",
        "full_name": "Test User",
    })
    assert res.status_code == 201
    assert res.json()["username"] == "testuser1"


def test_register_duplicate_username(client):
    client.post("/api/auth/register", json={
        "username": "dupeuser",
        "email": "dupe1@example.com",
        "password": "SecurePass123",
    })
    res = client.post("/api/auth/register", json={
        "username": "dupeuser",
        "email": "dupe2@example.com",
        "password": "SecurePass123",
    })
    assert res.status_code == 400


def test_login_success(client):
    client.post("/api/auth/register", json={
        "username": "loginuser",
        "email": "loginuser@example.com",
        "password": "SecurePass123",
    })
    res = client.post("/api/auth/login", json={
        "username": "loginuser", "password": "SecurePass123",
    })
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_wrong_password(client):
    client.post("/api/auth/register", json={
        "username": "wrongpassuser",
        "email": "wrongpass@example.com",
        "password": "SecurePass123",
    })
    res = client.post("/api/auth/login", json={
        "username": "wrongpassuser", "password": "WrongPassword",
    })
    assert res.status_code == 401


def test_get_me_requires_auth(client):
    res = client.get("/api/auth/me")
    assert res.status_code == 401


def test_get_me_with_token(client):
    client.post("/api/auth/register", json={
        "username": "meuser",
        "email": "meuser@example.com",
        "password": "SecurePass123",
    })
    login_res = client.post("/api/auth/login", json={
        "username": "meuser", "password": "SecurePass123",
    })
    token = login_res.json()["access_token"]

    res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["username"] == "meuser"
