"""
Tests for the image detection endpoint. Uses a tiny generated JPEG so
the test doesn't depend on external fixture files; assumes the YOLO
fallback (yolov8n.pt) is loaded since no custom weights exist yet.
"""
import io
import pytest
from PIL import Image


def _get_token(client, username="detectuser"):
    client.post("/api/auth/register", json={
        "username": username,
        "email": f"{username}@example.com",
        "password": "SecurePass123",
    })
    res = client.post("/api/auth/login", json={"username": username, "password": "SecurePass123"})
    return res.json()["access_token"]


def _dummy_image_bytes():
    img = Image.new("RGB", (320, 240), color=(120, 120, 120))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf


def test_detect_image_requires_auth(client):
    res = client.post("/api/detect/image", files={"file": ("test.jpg", _dummy_image_bytes(), "image/jpeg")})
    assert res.status_code == 401


@pytest.mark.skipif(True, reason="Requires YOLO weights + torch installed; enable in CI with model present")
def test_detect_image_success(client):
    token = _get_token(client)
    res = client.post(
        "/api/detect/image",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.jpg", _dummy_image_bytes(), "image/jpeg")},
    )
    assert res.status_code == 200
    data = res.json()
    assert "is_defective" in data
    assert "detections" in data


def test_detect_image_rejects_bad_content_type(client):
    token = _get_token(client, "badtypeuser")
    res = client.post(
        "/api/detect/image",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.txt", io.BytesIO(b"not an image"), "text/plain")},
    )
    assert res.status_code == 400
