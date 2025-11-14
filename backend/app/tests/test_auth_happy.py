import time

def test_register_login_me_refresh_logout_flow(client):
    # Register
    r = register(client)
    assert r.status_code in (200, 201)
    # Login
    r = login(client)
    assert r.status_code == 200
    tokens = r.json()
    assert "access_token" in tokens and "refresh_token" in tokens
    at1 = tokens["access_token"]
    rt1 = tokens["refresh_token"]

    # Access protected
    r = me(client, at1)
    assert r.status_code == 200
    profile = r.json()
    assert profile["email"] == "alice@example.com"

    # Refresh rotation
    r = refresh(client, rt1)
    assert r.status_code == 200
    tokens2 = r.json()
    assert tokens2["access_token"] != at1
    assert tokens2["refresh_token"] != rt1
    at2 = tokens2["access_token"]
    rt2 = tokens2["refresh_token"]

    # Old refresh should now be invalid (rotation)
    r = refresh(client, rt1)
    assert r.status_code in (401, 400)

    # New access works
    r = me(client, at2)
    assert r.status_code == 200

    # Logout revokes refresh
    r = logout(client, refresh_token=rt2)
    assert r.status_code in (200, 204)

    # Cannot refresh after logout
    r = refresh(client, rt2)
    assert r.status_code in (401, 400)
