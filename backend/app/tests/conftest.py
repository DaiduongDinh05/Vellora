

import os
import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool


os.environ.setdefault("GOOGLE_CLIENT_ID", "test-google-client-id")
os.environ.setdefault("GOOGLE_CLIENT_SECRET", "test-google-client-secret")
os.environ.setdefault("GOOGLE_REDIRECT_URI", "http://test/oauth/google/callback")


os.environ.setdefault("OAUTH_GOOGLE_CLIENT_ID", "test-google-client-id")
os.environ.setdefault("OAUTH_GOOGLE_CLIENT_SECRET", "test-google-client-secret")
os.environ.setdefault("OAUTH_GOOGLE_REDIRECT_URI", "http://test/oauth/google/callback")

os.environ.setdefault("ENV", "test")
os.environ.setdefault("JWT_SECRET_KEY", "this_is_a_very_long_test_secret_key_32_chars_min")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRES_MIN", "1")
os.environ.setdefault("REFRESH_TOKEN_EXPIRES_MIN", "5")

# Force SQLite for tests
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"
os.environ["DATABASE_URL"] = TEST_DB_URL

# Dummy Google OAuth so provider registry is happy
os.environ.setdefault("GOOGLE_CLIENT_ID", "test-google-client-id")
os.environ.setdefault("GOOGLE_CLIENT_SECRET", "test-google-client-secret")
os.environ.setdefault("GOOGLE_REDIRECT_URI", "http://test/oauth/google/callback")

from app.main import app as fastapi_app
from app.core.base import Base
from app.infra.db import get_db  


try:
    from app.core.settings import get_settings as _get_settings_dep, Settings  
except Exception:
    
    _get_settings_dep = None
    Settings = None

# Event Loop
@pytest_asyncio.fixture(scope="session")
def event_loop():
    """One session-scoped loop so the async engine/sessions share it."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# Engine and Sessions 
@pytest_asyncio.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(
        TEST_DB_URL,
        future=True,
        echo=False,
        poolclass=StaticPool,  # keep one in-memory DB alive for the session
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()

@pytest_asyncio.fixture(scope="session")
async def session_maker(async_engine):
    return async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)

@pytest_asyncio.fixture()
async def async_session(session_maker):
    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def patch_app_db_layer(async_engine, session_maker):
    """
    If app.infra.db defines module-level engine/sessionmaker, point them to the test engine.
    This prevents any code path from creating a Postgres asyncpg engine.
    """
    try:
        from app import infra as _infra
        from app.infra import db as db_module
    except Exception:
        return  

    # Patch globals commonly used in FastAPI templates
    if hasattr(db_module, "engine"):
        db_module.engine = async_engine  # use our SQLite engine
    if hasattr(db_module, "AsyncSessionLocal"):
        db_module.AsyncSessionLocal = session_maker

    # Some code binds metadata globally; ensure it's not bound to anything stale
    try:
        Base.metadata.bind = None  # use engine passed to run_sync, not a stale bind
    except Exception:
        pass

@pytest.fixture()
def app(async_session):
    async def _override_db():
        # yield an AsyncSession from our sessionmaker
        yield async_session

    fastapi_app.dependency_overrides[get_db] = _override_db

    if _get_settings_dep and Settings:
        def _override_settings() -> Settings:
            # Construct Settings with test DB + dummy oauth
            # Fill any required fields your app expects.
            return Settings(
                DATABASE_URL=TEST_DB_URL,
                JWT_SECRET_KEY=os.environ["JWT_SECRET_KEY"],
                JWT_ALGORITHM=os.environ.get("JWT_ALGORITHM", "HS256"),
                ACCESS_TOKEN_EXPIRES_MIN=int(os.environ.get("ACCESS_TOKEN_EXPIRES_MIN", "1")),
                REFRESH_TOKEN_EXPIRES_MIN=int(os.environ.get("REFRESH_TOKEN_EXPIRES_MIN", "5")),
                GOOGLE_CLIENT_ID=os.environ["GOOGLE_CLIENT_ID"],
                GOOGLE_CLIENT_SECRET=os.environ["GOOGLE_CLIENT_SECRET"],
                GOOGLE_REDIRECT_URI=os.environ["GOOGLE_REDIRECT_URI"],
            )
        fastapi_app.dependency_overrides[_get_settings_dep] = _override_settings

    return fastapi_app

@pytest_asyncio.fixture()
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

# -------------------- Optional: clean-slate helper --------------------
@pytest_asyncio.fixture()
async def reset_database(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
