import pytest

pytestmark = pytest.mark.asyncio


async def test_duplicate_registration_returns_conflict(client):
    payload = {"email": "duplicate@example.com", "password": "Secret123!", "full_name": "User One"}
    first_resp = await client.post("/api/v1/auth/register", json=payload)
    assert first_resp.status_code == 201

    second_resp = await client.post("/api/v1/auth/register", json=payload)
    assert second_resp.status_code == 409


async def test_login_with_invalid_credentials(client):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "invalid@example.com", "password": "Secret123!", "full_name": "User One"},
    )

    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "invalid@example.com", "password": "WrongPassword!"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401


async def test_me_requires_bearer_token(client):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401


async def test_refresh_with_invalid_token(client):
    response = await client.post("/api/v1/auth/refresh", json={"refresh_token": "not-a-real-token"})
    assert response.status_code == 401
