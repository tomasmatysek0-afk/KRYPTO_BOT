# PROJECT STATE

## Current Slice

- Phase: 04 - Data source decision ADR local/provisional slice
- State: TODO
- Agent: architect-agent + data-agent
- Started: 2026-06-21 11:55
- Branch: main
- Base commit: 21aa343
- Current mode: `NO_DOCKER_LOCAL_MODE`
- Docker status: `DEFERRED_DOCKER_REQUIRED`

## Last PASS/FAIL

- Last validation: 2026-06-21 11:55
- Result: PARTIAL - Phase 03b local/mock Data Parity Gate completed; real data parity remains deferred, not passed.
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

- Phase 04 can proceed as a provisional local ADR.
- Allowed locally: document the provisional data-source decision and explicitly block final strategy validation until real Coinbase/Freqtrade parity checks run.
- Deferred: Docker Compose validation, Freqtrade container execution, Docker import smoke tests, and Freqtrade dry-run runtime.

## Files Changed In Current Slice

- None yet for Phase 04.

## Tests And Checks

- PASS - `[LOCAL_VENV] .\.venv\Scripts\python.exe -m pytest`
- PASS - `[LOCAL_VENV] .\.venv\Scripts\ruff.exe check .`
- PASS - `[LOCAL_VENV] .\.venv\Scripts\python.exe -m pip check`
- PASS - `[HOST_POWERSHELL] powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 no-secrets`
- PASS - `[HOST_POWERSHELL] git diff --check` with line-ending warnings only.
- PASS - `[LOCAL_VENV] .\.venv\Scripts\python.exe -m pytest tests\test_no_live_execution.py`
- DEFERRED_DOCKER_REQUIRED - `[HOST_POWERSHELL] docker compose config`
- DEFERRED_DOCKER_REQUIRED - `[DOCKER_FREQTRADE] docker compose run --rm freqtrade --help`
- DEFERRED_DOCKER_REQUIRED - `[DOCKER_FREQTRADE] docker compose run --rm freqtrade list-exchanges`
- DEFERRED_DOCKER_REQUIRED - `[DOCKER_FREQTRADE] docker compose run --rm freqtrade list-pairs --exchange coinbase --quote USD --print-json`
- DEFERRED_DOCKER_REQUIRED - `[DOCKER_FREQTRADE] docker compose run --rm freqtrade --version`
- PASS - `[LOCAL_VENV] .\.venv\Scripts\python.exe -m pytest tests\test_data_parity.py`
- PASS - `[LOCAL_VENV] .\.venv\Scripts\python.exe scripts\compare_coinbase_data_sources.py`

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
- Safe resume instruction: Read `CODEX_MASTER_PLAN.md`, `AGENTS.md`, `LOG.md`, and this file; commit/push Phase 03b if needed; then continue Phase 04 with a provisional data-source ADR that preserves the real-data parity gate.
- Recommended commit message: `phase-03b: add offline data parity gate`

## Risks

- Docker/Freqtrade runtime behavior remains unvalidated locally.
- Phase 03 is only `PARTIAL_RESEARCH_DOCKER_DEFERRED` until Docker list-exchanges/list-pairs/version checks run.
- Phase 03b is only `LOCAL_MOCK_DONE_REAL_DATA_DEFERRED` until real Coinbase/Freqtrade data parity runs.
- Docker deferral must not weaken no-live-trading, no-secrets, audit, guard, or kill-switch requirements.
