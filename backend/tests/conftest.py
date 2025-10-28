import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4


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
