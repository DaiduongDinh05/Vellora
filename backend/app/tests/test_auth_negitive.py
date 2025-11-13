import jwt
from app.config import get_settings

def test_login_wrong_password(client):
    register(client, email="bob@example.com", password="CorrectHorse1!")
    r = login(client, email="bob@example.com", password="WrongPass1!")
    assert r.status_code in (400, 401)

def test_protected_requires_bearer(client):
    resp = client.get("/api/v1/auth/me")
    assert resp.status_code == 401

def test_tampered_jwt_signature(client):
    register(client, email="carol@example.com", password="StrongP@ss1!")
    r = login(client, email="carol@example.com")
    at = r.json()["access_token"]

    # Replace signature with junk (simulate tamper)
    parts = at.split(".")
    fake = parts[0] + "." + parts[1] + ".xxxx"
    resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {fake}"})
    assert resp.status_code == 401

def test_expired_access_token(client):
    register(client, email="dave@example.com", password="Aaa1!aaaa")
    r = login(client, email="dave@example.com")
    tokens = r.json()
    at = tokens["access_token"]

    # Wait for 1–2s 
    import time
    time.sleep(2)

    resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {at}"})
    assert resp.status_code in (401, 403)

def test_refresh_reuse_detection(client):
    register(client, email="erin@example.com", password="Aaa1!aaaa")
    r = login(client, email="erin@example.com")
    rt1 = r.json()["refresh_token"]

    # First refresh (valid)
    r = refresh(client, rt1)
    assert r.status_code == 200
    rt2 = r.json()["refresh_token"]

    # Reuse the first (should fail due to rotation)
    r = refresh(client, rt1)
    assert r.status_code in (401, 400)

    # New one still valid
    r = refresh(client, rt2)
    assert r.status_code == 200
