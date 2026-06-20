# packaging_app_architecture

## Purpose

Track packaging and application architecture rules.

## Current conclusions

The project must become an installable Python package, not a loose script collection.

## Findings

### 2026-06-20 - Bootstrap
Source:
- CODEX_MASTER_PLAN.md

Summary:
Package scaffolding, `pyproject.toml`, and CLI smoke tests are Phase 00b scope.

Decision impact:
Phase 00 creates directories only; no package code yet.

Open questions:
- None for Phase 00.

### 2026-06-20 - Phase 00b packaging baseline
Source:
- CODEX_MASTER_PLAN.md
- docs/PACKAGING.md

Summary:
The project uses a `src/` package layout with `hatchling` as the build backend and standard-library-only runtime code in Phase 00b.

Decision impact:
Runtime dependencies remain empty. Dev dependencies are limited to the allowed bootstrap stack and are locked separately.

Open questions:
- None.
