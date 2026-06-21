# PROJECT STATE

## Current Slice

- Phase: 03 - Coinbase/Freqtrade capability check local research slice
- State: TODO
- Agent: data-agent
- Started: 2026-06-21 11:43
- Branch: main
- Base commit: 46eba0b
- Current mode: `NO_DOCKER_LOCAL_MODE`
- Docker status: `DEFERRED_DOCKER_REQUIRED`

## Last PASS/FAIL

- Last validation: 2026-06-21 11:43
- Result: PASS - Phase 02 local/static checks passed; Docker-dependent checks are `DEFERRED_DOCKER_REQUIRED`, not passed.
- Current decision: local work continues without Docker; Docker-dependent acceptance criteria are deferred, not passed.

## Open Questions

- None for current local no-Docker work.

## Current Decisions

- Local development continues in `NO_DOCKER_LOCAL_MODE`.
- Docker remains part of the architecture and must be revalidated later.
- Docker-dependent acceptance criteria are marked `DEFERRED_DOCKER_REQUIRED`; they are not passed.
- Do not ask the user to install Docker/WSL again while this mode is active.
- Do not attempt privileged installation commands.
- No API keys, secrets, live trading, futures, leverage, shorts, databases, caches, or runtime artifacts may be committed.

## Next Safe Local Phase

- Phase 03 can proceed as local research and documentation.
- Allowed locally: verify current Coinbase/Freqtrade/CCXT capability from official sources, document findings, update runbook/data-source policy notes, and keep all tests offline by default.
- Deferred: Docker Compose validation, Freqtrade container execution, Docker import smoke tests, and Freqtrade dry-run runtime.

## Files Changed In Current Slice

- None yet for Phase 03.

## Tests And Checks

- PASS - `[LOCAL_VENV] .\.venv\Scripts\python.exe -m pytest`
- PASS - `[LOCAL_VENV] .\.venv\Scripts\ruff.exe check .`
- PASS - `[LOCAL_VENV] .\.venv\Scripts\python.exe -m pip check`
- PASS - `[HOST_POWERSHELL] powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 no-secrets`
- PASS - `[HOST_POWERSHELL] git diff --check` with line-ending warnings only.
- PASS - `[LOCAL_VENV] .\.venv\Scripts\python.exe -m pytest tests\test_no_live_execution.py`
- DEFERRED_DOCKER_REQUIRED - `[HOST_POWERSHELL] docker compose config`
- DEFERRED_DOCKER_REQUIRED - `[DOCKER_FREQTRADE] docker compose run --rm freqtrade --help`

## Future Docker-Capable Resume Instructions

On a Docker-capable machine, run a dedicated Docker revalidation slice before marking Docker criteria complete:

```powershell
# [HOST_POWERSHELL]
docker --version

# [HOST_POWERSHELL]
docker compose version

# [HOST_POWERSHELL]
wsl --status

# [HOST_POWERSHELL]
docker compose config

# [DOCKER_FREQTRADE]
docker compose run --rm freqtrade --help
```

Then verify Docker package import, Freqtrade strategy import without `sys.path.append`, `dry_run=true`, no real API keys, no secrets, and no live order path. Update `LOG.md`, `PROJECT_STATE.md`, and the phase tracker with PASS/FAIL.

## Quota-Safe Resume Fields

- Next deterministic command: `[HOST_POWERSHELL] git status --short --branch`
- Safe resume instruction: Read `CODEX_MASTER_PLAN.md`, `AGENTS.md`, `LOG.md`, and this file; commit/push the Phase 02 local/static slice if needed; then continue Phase 03 as local research only.
- Recommended commit message: `phase-02: add portable freqtrade skeleton`

## Risks

- Docker/Freqtrade runtime behavior remains unvalidated locally.
- Phase 02 can only complete local static/offline acceptance criteria until Docker is available.
- Docker deferral must not weaken no-live-trading, no-secrets, audit, guard, or kill-switch requirements.
