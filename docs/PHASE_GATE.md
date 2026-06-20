# Phase Gate

## Purpose

Phase gates prevent premature movement toward live trading.

## General Gate Rules

- A phase may pass only when its acceptance criteria are met.
- `LOG.md` and `PROJECT_STATE.md` must be updated after each slice.
- Relevant tests or validation checks must run.
- Secrets, `.env`, `.venv`, databases, caches, and runtime artifacts must not be committed.
- If a hard-stop occurs, record it in `LOG.md` and stop.

## Live Trading Gate

Phase 18 is locked. It may not start without explicit user approval and a separate commit that intentionally changes the live pilot state.

## Current Gate State

Phase 00 is in progress. All later phases are blocked until Phase 00 passes.
