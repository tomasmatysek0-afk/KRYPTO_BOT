# Coding Standards

## Purpose

These standards keep the project importable, typed, testable, and auditable.

## Python Rules

- Use Python 3.11 or newer.
- Put application logic under `src/coinbase_freqtrade_guarded_bot/`.
- Give every module a module docstring.
- Give every public function, class, and method type hints.
- Give public functions and classes concise docstrings.
- Use dataclasses or typed models for domain data instead of loose dictionaries.
- Keep modules small and focused on one responsibility.
- Do not use `print()` in business logic; CLI presentation code may write user-facing output.
- Do not run network calls or trading side effects at import time.
- Do not use `sys.path.append` hacks.
- Do not read `.env` directly inside business logic.
- Fail closed when a risk, data, audit, or reconciliation state is unknown.

## Tests

- New behavior needs tests.
- Unit tests must not perform real network calls.
- Default tests run with sockets disabled through `pytest-socket`.
- Guard, reconciliation, data parity, metrics, and tax code require deterministic edge-case tests.

## Current Phase

Phase 00b creates only package skeleton, CLI placeholders, and smoke tests. Trading, data parity, guard, tax, and reporting behavior are implemented in later phases.
