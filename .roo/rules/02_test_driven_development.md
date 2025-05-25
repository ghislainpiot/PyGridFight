# Test-Driven Development (TDD)

## Red-Green-Refactor Cycle
- All new functionality or bug fixes must start with a failing test (Red)
- Write code to make the test pass (Green)
- Refactor code and tests for clarity and efficiency

## Test Execution
- Tests must be run frequently during development using `uv run pytest`
- All tests must pass before committing code

## Test Coverage and Quality
- All critical paths and business logic must be covered by tests
- Write focused unit tests that test single concerns
- Avoid testing multiple concerns in a single test case