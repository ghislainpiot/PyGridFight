# Testing Strategy

## Unit Testing
- Test individual classes, methods, and functions in isolation within each Bounded Context
- Use mocks/stubs for external dependencies to ensure unit tests are fast and reliable
- Unit tests for a module should reside in corresponding test files within the `tests/` directory, mirroring the application's structure

## Integration Testing
- Test interactions between components or services within a Bounded Context or between closely coupled Bounded Contexts
- Avoid over-mocking; allow real components to interact where feasible for the integration test's purpose
- Follow the Context Map defined in `documents/PyGridFight_Architecture.md`

## API Testing (WebSocket)
- Test WebSocket communication, message validation (schemas), and state updates as perceived by a client
- Cover connection handshake, player actions (move, collect, purchase), spectator mode, and error message handling
- Utilize appropriate testing libraries for WebSocket clients if necessary

## Test Data
- Use clear and representative test data
- Avoid magic numbers or obscure values in tests
- Use named constants or descriptive variables