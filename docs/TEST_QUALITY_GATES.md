# Test Quality Gates

## Required Gates

- `python -m pytest`
- `python -m ruff check .`
- import smoke tests
- CLI smoke tests
- no-secret smoke scan
- default socket ban through `pytest-socket --disable-socket`

## Coverage

Phase 00b configures `pytest-cov`. Global fail-under thresholds start later when non-trivial guard, data, tax, and metrics code exists.

Critical layers will eventually target high branch coverage:

- guard layer;
- data parity;
- tax layer;
- reconciliation;
- research metrics.

## Network Tests

Tests requiring network must be marked as integration tests and must not be part of the default unit-test path.
