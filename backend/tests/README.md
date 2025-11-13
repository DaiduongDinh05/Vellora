# Tests

This directory contains comprehensive tests for the Vellora backend application.

## Test Structure

```
tests/
├── modules/           # Unit tests (mocked dependencies, fast)
│   ├── expenses/
│   │   ├── test_schemas.py
│   │   ├── test_service.py
│   │   ├── test_repository.py
│   │   └── test_router.py
│   ├── rate_categories/
│   ├── rate_customizations/
│   └── trips/
│       ├── test_schemas.py
│       ├── test_service.py
│       ├── test_repository.py
│       ├── test_router.py
│       ├── test_distance.py  # Distance conversion utilities
│       └── test_crypto.py    # Address encryption utilities
├── integration/       # Integration tests (real database, slower)
│   ├── conftest.py   # Test database fixtures (SQLite in-memory)
│   └── test_trip_repository.py
└── conftest.py       # Shared test fixtures


## Running Tests

### Install Test Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install test dependencies (includes pytest, pytest-asyncio, pytest-cov, pytest-mock, aiosqlite)
pip install -r requirements-test.txt
```

### Run Unit Tests Only (Fast, Default)

```bash
# Run all unit tests
pytest tests/modules/ -v

# Run specific module unit tests
pytest tests/modules/trips/ -v

# Run with coverage
pytest tests/modules/trips/ --cov=app.modules.trips --cov-report=term-missing
```

### Run Integration Tests (Slower, Requires DB)

```bash
# Run all integration tests
pytest tests/integration/ -v -m integration

# Run specific integration test file
pytest tests/integration/test_trip_repository.py -v

# Skip integration tests when running all tests
pytest -v -m "not integration"
```

### Run All Tests (Unit + Integration)

```bash
# Run everything
pytest -v

# Run with coverage for all modules
pytest --cov=app.modules --cov-report=term-missing

# Run and stop on first failure
pytest -x

# Run with verbose output and show print statements
pytest -v -s
```

## Test Design Principles

### 1. AAA Pattern
All tests follow the **Arrange-Act-Assert** pattern:
```python
@pytest.mark.asyncio
async def test_create_expense_success(self, service, mock_expense):
    # Arrange: Set up test data and mocks
    trip_id = uuid4()
    expense_repo.get_by_trip_and_type.return_value = None
    
    # Act: Execute the function under test
    result = await service.create_expense(trip_id, valid_dto)
    
    # Assert: Verify the results
    assert result == mock_expense
    expense_repo.save.assert_called_once()
```

### 2. Isolation via Mocking
Unit tests mock all external dependencies (database, repositories, external services):
```python
@pytest.fixture
def mock_trip_repo(mocker):
    return mocker.AsyncMock(spec=TripRepo)

@pytest.fixture
def service(mock_trip_repo, mock_expense_repo):
    return TripsService(trip_repo=mock_trip_repo, expense_repo=mock_expense_repo)
```

### 3. Descriptive Names
Test names follow the pattern: `test_<method>_<scenario>`
```python
test_create_expense_success
test_create_expense_trip_not_found
test_create_expense_duplicate_type
test_create_expense_negative_amount
```

## Maintenance

### Adding New Tests
1. Follow existing test structure and naming conventions
2. Use appropriate fixtures from `conftest.py`
3. Mock external dependencies in unit tests
4. Add integration tests for complex database operations
5. Run tests locally before committing