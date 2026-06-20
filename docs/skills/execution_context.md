# execution_context

## Purpose

Track command execution context rules.

## Current conclusions

Every shell command must be labeled as `[HOST_POWERSHELL]`, `[LOCAL_VENV]`, `[DOCKER_APP]`, or `[DOCKER_FREQTRADE]`.

## Findings

### 2026-06-20 - Bootstrap
Source:
- CODEX_MASTER_PLAN.md

Summary:
Phase 00 uses host PowerShell only. Python and Docker commands are deferred until their phases.

Decision impact:
RUNBOOK starts with the command context catalog.

Open questions:
- None for Phase 00.

### 2026-06-20 - Phase 00b command catalog
Source:
- CODEX_MASTER_PLAN.md
- docs/EXECUTION_CONTEXT.md
- scripts/dev.ps1

Summary:
Phase 00b introduces a Windows-first `scripts/dev.ps1` command catalog and keeps local Python commands under `[LOCAL_VENV]`.

Decision impact:
Docker commands are deferred to Phase 02; local package install, pytest, ruff, and CLI help run in the local venv.

Open questions:
- None.
