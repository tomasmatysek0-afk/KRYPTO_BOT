# dependency_review

## Purpose

Track dependency choices, license review, pinning, lock status, and security notes.

## Current conclusions

No dependencies have been added in Phase 00.

## Findings

### 2026-06-20 - Bootstrap
Source:
- CODEX_MASTER_PLAN.md

Summary:
The project prefers the standard library or compatible active packages. New dependencies require review and lock files.

Decision impact:
Phase 00 adds no Python dependencies.

Open questions:
- None for Phase 00.

### 2026-06-20 - Phase 00b allowed bootstrap stack
Source:
- CODEX_MASTER_PLAN.md
- pyproject.toml

Summary:
Phase 00b uses only the allowed bootstrap/dev stack: hatchling, pytest, pytest-cov, pytest-socket, and ruff. No runtime dependency is added.

Decision impact:
These packages must be exact-pinned in `requirements-dev.lock` after local install. Runtime lock remains empty unless installation introduces runtime dependencies.

Open questions:
- Exact installed versions will be recorded after lock generation.

### 2026-06-20 - Phase 00b exact dependency review
Source:
- `pyproject.toml`
- `requirements-dev.lock`
- `[LOCAL_VENV] python -m pip show hatchling pytest pytest-cov pytest-socket ruff`
- `[LOCAL_VENV] python -m pip check`

Summary:
Direct Phase 00b dev dependencies installed and reviewed:
- `hatchling==1.30.1`, MIT, build backend and packaging support.
- `pytest==8.4.2`, MIT, unit test runner.
- `pytest-cov==7.1.0`, MIT, coverage reporting.
- `pytest-socket==0.8.0`, MIT, default socket ban for unit tests.
- `ruff==0.15.18`, MIT, linting.

Transitive dependencies are exact-pinned in `requirements-dev.lock` and mirrored in `constraints.txt`. Runtime dependencies remain empty in `requirements.lock`.

Decision impact:
The dev stack satisfies the bootstrap minimal dependency policy. No runtime trading, Coinbase, ORM, retry, ML, or UI dependency is introduced.

Open questions:
- None.
