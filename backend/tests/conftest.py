import pytest
import os
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
import os


if "FERNET_KEY" not in os.environ:
    from cryptography.fernet import Fernet
    os.environ["FERNET_KEY"] = Fernet.generate_key().decode()

if "DATABASE_URL" not in os.environ:
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

if "FERNET_KEY" not in os.environ:
    from cryptography.fernet import Fernet
    os.environ["FERNET_KEY"] = Fernet.generate_key().decode()

if "DATABASE_URL" not in os.environ:
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
@pytest.fixture
def mock_db_session():
    """Fixture for mocking AsyncSession"""
    session = AsyncMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    session.scalar = AsyncMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def sample_trip_id():
    """Fixture providing a sample trip UUID"""
    return uuid4()


@pytest.fixture
def sample_expense_id():
    """Fixture providing a sample expense UUID"""
    return uuid4()
