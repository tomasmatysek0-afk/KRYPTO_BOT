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
