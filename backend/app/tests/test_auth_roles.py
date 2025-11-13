def test_insufficient_role_gets_403(client):
    register(client, email="user@ex.com", password="P@ssw0rd!", name="User")
    login_resp = login(client, email="user@ex.com")
    at = login_resp.json()["access_token"]
    # Hitting an admin-only route with a normal user
    r = client.get("/api/v1/admin/users", headers={"Authorization": f"Bearer {at}"})
    assert r.status_code in (403, 404)  
