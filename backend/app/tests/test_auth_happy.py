import pytest
from sqlalchemy import select

from app.modules.auth.models import OAuthAccount
from app.modules.auth.providers import registry
from app.modules.auth.providers.base import OAuthProviderBase
from app.modules.auth.providers.types import OAuthToken, OAuthUserInfo

pytestmark = pytest.mark.asyncio


async def test_register_login_refresh_logout_flow(client):
    email = "test.user@example.com"
    password = "SecretPass123!"

    register_response = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "full_name": "Test User"},
    )
    assert register_response.status_code == 201
    register_data = register_response.json()
    assert register_data["user"]["email"] == email
    access_token = register_data["tokens"]["access_token"]
    refresh_token = register_data["tokens"]["refresh_token"]

    me_response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == email

    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert login_data["user"]["email"] == email
    login_refresh_token = login_data["tokens"]["refresh_token"]

    refresh_response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": login_refresh_token},
    )
    assert refresh_response.status_code == 200
    refreshed_token = refresh_response.json()["tokens"]["refresh_token"]

    logout_response = await client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": refreshed_token},
    )
    assert logout_response.status_code == 204

    refresh_after_logout = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refreshed_token},
    )
    assert refresh_after_logout.status_code == 401


class _StubProvider(OAuthProviderBase):
    @property
    def name(self) -> str:
        return "google"

    def build_authorization_url(self, *, state: str, redirect_uri: str | None = None) -> str:
        return f"https://stub.example.com/auth?state={state}"

    async def exchange_code(self, *, code: str, redirect_uri: str | None = None) -> OAuthToken:
        assert code == "dummy-code"
        return OAuthToken(
            access_token="stub-access",
            refresh_token="stub-refresh",
            token_type="Bearer",
            expires_in=3600,
            scope="openid email profile",
        )

    async def fetch_user_info(self, token: OAuthToken) -> OAuthUserInfo:
        assert token.access_token == "stub-access"
        return OAuthUserInfo(
            subject="stub-subject",
            email="stub@example.com",
            full_name="Stub User",
            email_verified=True,
        )


async def test_google_oauth_flow(client, session_maker, monkeypatch):
    def _get_stub_provider(_: str) -> _StubProvider:
        return _StubProvider(
            client_id="stub-client-id",
            client_secret="stub-client-secret",
            redirect_uri="http://testserver/api/v1/auth/providers/google/callback",
            scopes=["openid", "email", "profile"],
        )

    monkeypatch.setattr(registry, "get_provider", _get_stub_provider)

    authorize_response = await client.get("/api/v1/auth/providers/google/authorize")
    assert authorize_response.status_code == 200
    authorize_data = authorize_response.json()
    state = authorize_data["state"]
    assert state
    assert authorize_data["authorization_url"].startswith("https://stub.example.com/auth")

    callback_response = await client.get(
        "/api/v1/auth/providers/google/callback",
        params={"code": "dummy-code", "state": state},
    )
    assert callback_response.status_code == 200
    callback_data = callback_response.json()
    assert callback_data["user"]["email"] == "stub@example.com"
    assert "access_token" in callback_data["tokens"]

    async with session_maker() as session:
        result = await session.execute(select(OAuthAccount))
        accounts = result.scalars().all()
    assert len(accounts) == 1
    account = accounts[0]
    assert account.provider == "google"
    assert account.email == "stub@example.com"
