# Quick Start Guide - Running Tests

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_activities.py -v

# Run with real-time output
pytest tests/ -v -s

# Run and stop on first failure
pytest tests/ -x

# Run specific test class
pytest tests/test_signup.py::TestSignup -v

# Run specific test
pytest tests/test_signup.py::TestSignup::test_successful_signup_adds_participant -v
```

## Test Structure

Each test file contains a test class organized by endpoint:

```
tests/
├── test_activities.py       → TestGetActivities class
├── test_signup.py           → TestSignup class
└── test_unregister.py       → TestUnregister class
```

## Understanding Test Names

Test names follow the pattern: `test_<action>_<condition>_<expected_result>`

Examples:
- `test_successful_signup_adds_participant` - When signup succeeds, participant is added
- `test_signup_duplicate_registration_prevented` - When duplicate signup attempted, it's rejected
- `test_unregister_nonexistent_participant_returns_400` - When unregistering unknown participant, 400 error

## AAA Pattern Reminder

Each test follows this structure:

```python
def test_name(self, client, reset_activities):
    # ARRANGE: Set up test data
    activity = "Chess Club"
    email = "student@example.edu"
    
    # ACT: Execute the action
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # ASSERT: Verify results
    assert response.status_code == 200
```

## Available Fixtures

- `client` - FastAPI TestClient instance
- `reset_activities` - Resets activities to initial state before/after test

## Coverage Status

✅ **20/20 tests passing**  
✅ **100% endpoint coverage**  
✅ **All error cases tested**  
✅ **All success paths tested**  

## Debugging Failed Tests

```bash
# Run with verbose output and full stack trace
pytest tests/test_signup.py -vv --tb=long

# Show print statements
pytest tests/ -v -s

# Run single test with verbose output
pytest tests/test_signup.py::TestSignup::test_successful_signup_adds_participant -vv
```

## CI/CD Integration

The test suite is ready for GitHub Actions CI/CD:

```yaml
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest tests/ -v
```

---

**Happy Testing! 🎉**
