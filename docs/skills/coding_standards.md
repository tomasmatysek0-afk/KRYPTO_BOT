# coding_standards

## Purpose

Track coding standards for the Python application.

## Current conclusions

Application logic must be importable, typed, testable, and placed under `src/coinbase_freqtrade_guarded_bot/`.

## Findings

### 2026-06-20 - Bootstrap
Source:
- CODEX_MASTER_PLAN.md
- AGENTS.md

Summary:
No ad-hoc scripts for business logic. Public modules need module docstrings; public functions/classes need type hints and concise docstrings.

Decision impact:
Detailed coding standards document is scheduled for Phase 00b.

Open questions:
- None for Phase 00.

### 2026-06-20 - Phase 00b package standards
Source:
- CODEX_MASTER_PLAN.md
- docs/CODING_STANDARDS.md

Summary:
Phase 00b establishes Python 3.11+ package rules, module docstrings, type hints, no import-time side effects, no `sys.path.append`, and tests for new behavior.

Decision impact:
Application logic is directed to `src/coinbase_freqtrade_guarded_bot/`; CLI code remains presentation-only and contains no live trading command.

Open questions:
- None.
