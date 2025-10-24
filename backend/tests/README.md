# Tests

This directory contains comprehensive unit tests for the expenses module of the Vellora backend application.


## Running Tests

### Install Test Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install test dependencies
pip install -r requirements-test.txt
```

### Run All Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest tests/modules/<folder_name>/ --cov=app.modules.<folder_name> --cov-report=term-missing

# Run specific test file
pytest tests/modules/<folder_name>/<file_name>.py
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


### 3. Descriptive Names
Test names follow the pattern: `test_<method>_<scenario>`
```python
test_create_expense_success
test_create_expense_trip_not_found
test_create_expense_duplicate_type
```

## Maintenance

### Adding New Tests
1. Follow existing test structure and naming conventions
2. Use appropriate fixtures from `conftest.py`
5. Run tests locally before committing