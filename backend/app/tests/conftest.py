import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.config import settings
from app.core.base import Base
from app.infra.db import get_db
from app.main import app

# Ensure models are imported so metadata is populated
from app.modules.auth import models as auth_models  # noqa: F401
from app.modules.users import models as user_models  # noqa: F401


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
def session_maker(async_engine):
    return async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture
async def reset_database(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture
async def db_session(session_maker):
    async with session_maker() as session:
        yield session


@pytest.fixture
async def client(session_maker, reset_database):
    async def override_get_db():
        async with session_maker() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    settings.JWT_SECRET_KEY = "test-secret-key-32-bytes-long!!!"
    settings.OAUTH_PROVIDERS.google.client_id = "test-client-id"
    settings.OAUTH_PROVIDERS.google.client_secret = "test-client-secret"
    settings.OAUTH_PROVIDERS.google.redirect_uri = "http://testserver/api/v1/auth/providers/google/callback"

    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

    app.dependency_overrides.clear()
