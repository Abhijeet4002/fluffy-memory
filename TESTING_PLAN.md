# Backend Testing Plan - Mergington High School Activities API

## Overview
This document outlines the testing strategy for the FastAPI backend, including directory structure, test coverage, and implementation approach.

---

## Directory Structure

```
fluffy-memory/
├── src/
│   ├── app.py
│   └── static/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures and configuration
│   ├── test_activities.py          # Tests for GET /activities
│   ├── test_signup.py              # Tests for POST /activities/{name}/signup
│   └── test_unregister.py          # Tests for DELETE /activities/{name}/unregister
├── requirements.txt
└── pytest.ini
```

---

## Testing Dependencies to Add

Add these to `requirements.txt`:
- `pytest` - Testing framework
- `pytest-asyncio` - For async test support (optional, if using async endpoints)
- `httpx` - Already included, used as HTTP client for testing

No additional dependencies needed beyond what's already in the project!

---

## Test Coverage Plan

### 1. **test_activities.py** - GET /activities endpoint
Tests for retrieving all activities:
- ✅ Returns all activities with correct structure
- ✅ Participant list includes all signed-up students
- ✅ Max participants field is present
- ✅ Available spots calculation is correct
- ✅ Empty activities have empty participant lists

### 2. **test_signup.py** - POST /activities/{name}/signup endpoint
Tests for activity signup:
- ✅ Successful signup adds participant to activity
- ✅ Returns correct success message
- ✅ Prevents duplicate signups for same student
- ✅ Returns 400 error when student already signed up
- ✅ Returns 404 when activity doesn't exist
- ✅ Prevents signup when activity is at max capacity
- ✅ Returns 400 error when at capacity
- ✅ Handles email validation properly

### 3. **test_unregister.py** - DELETE /activities/{name}/unregister endpoint
Tests for activity unregistration:
- ✅ Successful unregister removes participant
- ✅ Returns correct success message
- ✅ Returns 404 when activity doesn't exist
- ✅ Returns 400 when participant not signed up
- ✅ Participant no longer appears in activity after removal

### 4. **conftest.py** - Shared fixtures
Reusable test utilities:
- FastAPI TestClient instance
- Sample activities fixture (fresh state before each test)
- Helper functions for common operations

---

## Testing Approach

### Test Client Setup
Use FastAPI's built-in `TestClient` from `starlette.testclient`:
```python
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)
```

### Fixtures Strategy
- **Fresh state**: Each test starts with clean activity data
- **Reusable fixtures**: Create fixtures for test activities and participants
- **Parametrized tests**: Use `@pytest.mark.parametrize` for testing multiple scenarios

### Test Isolation
- Use pytest fixtures to reset activities to initial state before each test
- Avoid cross-test dependencies
- Each test should be independent and runnable in any order

---

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_signup.py

# Run specific test
pytest tests/test_signup.py::test_successful_signup

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=html

# Run and stop on first failure
pytest -x

# Run only tests matching a pattern
pytest -k "signup"
```

---

## CI/CD Integration

Future GitHub Actions workflow will:
- Install dependencies
- Run pytest suite
- Generate coverage report
- Fail build if tests don't pass

---

## Edge Cases to Test

1. **Duplicate Registrations** - Already covered by test_signup.py
2. **Capacity Limits** - Already covered by test_signup.py
3. **Non-existent Activities** - Already covered
4. **Non-existent Participants** - Already covered by test_unregister.py
5. **Case Sensitivity** - Activity names and emails (if relevant)
6. **Special Characters** - In email addresses
7. **Concurrent Requests** - (Future enhancement)

---

## Success Criteria

- ✅ All endpoints have test coverage
- ✅ All happy path scenarios tested
- ✅ All error cases tested
- ✅ All tests pass consistently
- ✅ Tests run in <5 seconds
- ✅ No cross-test dependencies
- ✅ Clear, descriptive test names

---

## Future Enhancements

- Add integration tests with actual database
- Add performance/load tests
- Add API contract tests
- Add security tests (SQL injection, etc.)
- Add test data factories for scalability
