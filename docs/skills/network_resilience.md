# network_resilience

## Purpose

Track network timeout, retry, backoff, and fail-closed rules.

## Current conclusions

Network calls must be separated from business logic and must not run in unit tests without mocks.

## Findings

### 2026-06-20 - Bootstrap
Source:
- CODEX_MASTER_PLAN.md

Summary:
No network client is implemented in Phase 00. Later network code must handle timeouts, 429, 5xx, and auth failures with bounded behavior.

Decision impact:
No network dependencies are added in Phase 00.

Open questions:
- None for Phase 00.

### 2026-06-20 - Phase 00b no-network unit baseline
Source:
- CODEX_MASTER_PLAN.md
- docs/NETWORK_RESILIENCE.md

Summary:
Unit tests are configured with sockets disabled by default. Network client implementation remains deferred.

Decision impact:
`pytest-socket` is part of the Phase 00b dev stack; tests added in this phase perform no real network calls.

Open questions:
- None.
