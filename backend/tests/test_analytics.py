"""
Tests for analytics endpoints — verifies auth requirement and default
(zero-data) response shape for a fresh user.
"""
def _get_token(client, username):
    client.post("/api/auth/register", json={
        "username": username,
        "email": f"{username}@example.com",
        "password": "SecurePass123",
    })
    res = client.post("/api/auth/login", json={"username": username, "password": "SecurePass123"})
    return res.json()["access_token"]


def test_dashboard_requires_auth(client):
    res = client.get("/api/analytics/dashboard")
    assert res.status_code == 401


def test_dashboard_empty_state(client):
    token = _get_token(client, "analyticsuser")
    res = client.get("/api/analytics/dashboard", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["total_inspections"] == 0
    assert data["defective_count"] == 0


def test_defect_frequency_empty(client):
    token = _get_token(client, "freqsuser")
    res = client.get("/api/analytics/defect-frequency", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json() == []


def test_trend_empty(client):
    token = _get_token(client, "trenduser")
    res = client.get("/api/analytics/trend?days=14", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json() == []
