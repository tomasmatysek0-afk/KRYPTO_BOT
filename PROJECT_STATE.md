# PROJECT STATE

## Current Slice

- Phase: 07 - Report layer
- State: LOCAL_OFFLINE_PASS
- Agent: quant-research-agent + sre-agent
- Started: 2026-06-21 13:29
- Branch: main
- Base commit: 9e2d4bc
- Current mode: `NO_DOCKER_LOCAL_MODE`
- Docker status: `DEFERRED_DOCKER_REQUIRED`

## Last PASS/FAIL

- Last validation: 2026-06-21 13:34
- Result: LOCAL_OFFLINE_PASS - Phase 07 deterministic local report bundle generation passes.
- Current decision: Phase 07 local work is complete. Do not mark Phase 08 passed because real Freqtrade/Docker dry-run runtime is unavailable and remains deferred, not passed.

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

- Phase 08 is next in the master plan, but it is dry-run/runtime work and remains constrained by Docker/Freqtrade availability.
- Allowed locally: documentation-only preparation if needed. Do not claim dry-run can start, restart tests passed, DB checks passed, or dry-run signals passed through guards.
- Deferred: real Freqtrade backtest execution, real strategy runtime loading, Docker-based Freqtrade backtest, Docker-based data download, real Coinbase/Freqtrade data parity, and dry-run runtime validation.

## Files Changed In Current Slice

- LOG.md
- PROJECT_STATE.md
- src/coinbase_freqtrade_guarded_bot/research/backtest_validation.py
- scripts/run_backtest_report.py
- tests/test_backtest_validation.py
- docs/RUNBOOK.md
- docs/skills/backtest_validation.md
- reports/backtests/2026-06-21_strategy_summary.md
- reports/backtests/2026-06-21_trades.csv
- reports/backtests/2026-06-21_metrics.json
- reports/backtests/2026-06-21_drawdown.csv
- reports/backtests/2026-06-21_walkforward.json
- reports/backtests/2026-06-21_montecarlo.json
- reports/backtests/2026-06-21_mock_backtest_report.md
- reports/backtests/2026-06-21_mock_backtest_report.json

## Tests And Checks

- PASS - `[LOCAL_VENV] .\.venv\Scripts\python.exe -m pytest` (69 tests)
- PASS - `[LOCAL_VENV] .\.venv\Scripts\ruff.exe check .`
- PASS - `[LOCAL_VENV] .\.venv\Scripts\python.exe -m pip check`
- PASS - `[HOST_POWERSHELL] powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 no-secrets`
- PASS - `[HOST_POWERSHELL] git diff --check` with line-ending warnings only.
- PASS - `[LOCAL_VENV] .\.venv\Scripts\python.exe -m pytest tests\test_no_live_execution.py`
- PASS - `[LOCAL_VENV] .\.venv\Scripts\python.exe -m pytest tests\test_backtest_validation.py`
- PASS - `[LOCAL_VENV] .\.venv\Scripts\ruff.exe check src\coinbase_freqtrade_guarded_bot\research\backtest_validation.py scripts\run_backtest_report.py tests\test_backtest_validation.py`
- PASS - `[LOCAL_VENV] .\.venv\Scripts\python.exe scripts\run_backtest_report.py`
- DEFERRED_DOCKER_REQUIRED - `[HOST_POWERSHELL] docker compose config`
- DEFERRED_DOCKER_REQUIRED - `[DOCKER_FREQTRADE] docker compose run --rm freqtrade --help`
- DEFERRED_DOCKER_REQUIRED - `[DOCKER_FREQTRADE] docker compose run --rm freqtrade list-exchanges`
- DEFERRED_DOCKER_REQUIRED - `[DOCKER_FREQTRADE] docker compose run --rm freqtrade list-pairs --exchange coinbase --quote USD --print-json`
- DEFERRED_DOCKER_REQUIRED - `[DOCKER_FREQTRADE] docker compose run --rm freqtrade --version`
- PASS - `[LOCAL_VENV] .\.venv\Scripts\python.exe -m pytest tests\test_data_parity.py`
- PASS - `[LOCAL_VENV] .\.venv\Scripts\python.exe scripts\compare_coinbase_data_sources.py`
- PASS - `[LOCAL_VENV] .\.venv\Scripts\python.exe -m pytest tests\test_strategy_sanity.py`
- PASS - `[LOCAL_VENV] .\.venv\Scripts\python.exe -m pytest tests\test_order_intent.py tests\test_risk_limits.py tests\test_kill_switch.py tests\test_audit_writer.py`

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
- Safe resume instruction: Read `CODEX_MASTER_PLAN.md`, `AGENTS.md`, `LOG.md`, and this file; commit/push Phase 07 if needed. Do not proceed to Phase 08 as passed in `NO_DOCKER_LOCAL_MODE`.
- Recommended commit message: `phase-07: add offline report bundle`

## Risks

- Docker/Freqtrade runtime behavior remains unvalidated locally.
- Phase 03 is only `PARTIAL_RESEARCH_DOCKER_DEFERRED` until Docker list-exchanges/list-pairs/version checks run.
- Phase 03b is only `LOCAL_MOCK_DONE_REAL_DATA_DEFERRED` until real Coinbase/Freqtrade data parity runs.
- Phase 05 is only `LOCAL_STATIC_DONE_RUNTIME_DEFERRED` until Freqtrade strategy runtime import/backtest runs.
- Docker deferral must not weaken no-live-trading, no-secrets, audit, guard, or kill-switch requirements.
- Phase 08 dry-run validation cannot be completed locally while Docker/Freqtrade runtime is unavailable.
