# Runbook

## Command Contexts

Every command must be marked with one execution context.

| Context | Use |
|---|---|
| `[HOST_POWERSHELL]` | Git repository operations, folders, Docker commands on Windows host. |
| `[LOCAL_VENV]` | Local Python package commands, pytest, ruff, mypy, CLI app commands. |
| `[DOCKER_APP]` | Future app container commands. |
| `[DOCKER_FREQTRADE]` | Future Freqtrade container commands. |

## Current Mode

Current local mode: `NO_DOCKER_LOCAL_MODE`.

Docker Desktop, Docker Compose, and WSL2 are not available on this workstation. Docker remains part of the target architecture, but Docker runtime validation is marked `DEFERRED_DOCKER_REQUIRED` until the project is run on a Docker-capable machine.

## Phase 00 Commands

```powershell
# [HOST_POWERSHELL]
git status --short --branch

# [HOST_POWERSHELL]
git remote -v

# [HOST_POWERSHELL]
git diff --stat
```

## Local No-Docker Command Catalog

Use these commands for current local work.

```powershell
# [HOST_POWERSHELL]
git status --short --branch

# [HOST_POWERSHELL]
git diff --stat

# [HOST_POWERSHELL]
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 no-secrets

# [LOCAL_VENV]
.\.venv\Scripts\python.exe -m pip install -e .[dev]

# [LOCAL_VENV]
.\.venv\Scripts\python.exe -m coinbase_freqtrade_guarded_bot --help

# [LOCAL_VENV]
.\.venv\Scripts\python.exe -m pytest

# [LOCAL_VENV]
.\.venv\Scripts\ruff.exe check .

# [LOCAL_VENV]
.\.venv\Scripts\python.exe -m pip check
```

Local unit tests must remain offline by default. Tests that need network access must be explicitly marked as integration tests and must not run in the default command.

## Phase 02 Local Static Checks

These checks are valid in `NO_DOCKER_LOCAL_MODE`.

```powershell
# [LOCAL_VENV]
.\.venv\Scripts\python.exe -m pytest tests\test_no_live_execution.py

# [LOCAL_VENV]
.\.venv\Scripts\python.exe -m pytest

# [LOCAL_VENV]
.\.venv\Scripts\ruff.exe check .

# [HOST_POWERSHELL]
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 no-secrets
```

The local tests verify:

- Freqtrade config files are JSON;
- `dry_run=true`;
- `trading_mode=spot`;
- no futures, margin, leverage, or shorts;
- Coinbase pair whitelist is BTC/USD and ETH/USD only;
- API server and Telegram are disabled;
- no API credential fields are present;
- Docker Compose uses relative repository mounts;
- no public port is exposed.

## Phase 03 Local Research Checks

These checks are valid in `NO_DOCKER_LOCAL_MODE`.

```powershell
# [HOST_POWERSHELL]
git status --short --branch

# [LOCAL_VENV]
.\.venv\Scripts\python.exe -m pytest

# [LOCAL_VENV]
.\.venv\Scripts\ruff.exe check .

# [HOST_POWERSHELL]
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 no-secrets
```

Phase 03 research output:

- `reports/research/2026-06-21_coinbase_freqtrade_capability.md`;
- `docs/DATA_SOURCE_POLICY.md`;
- `docs/skills/freqtrade_coinbase_ccxt.md`.

Local conclusion:

- CCXT documents Coinbase market/OHLCV methods.
- Freqtrade Coinbase support is not locally proven.
- Coinbase product IDs use dash notation such as `BTC-USD`.
- Freqtrade/CCXT pair candidates use slash notation such as `BTC/USD`.
- Coinbase Advanced Trade candle data is the candidate authoritative source if Data Parity Gate finds Freqtrade/CCXT mismatch.

Deferred Docker checks for Phase 03:

```powershell
# [DOCKER_FREQTRADE]
docker compose run --rm freqtrade list-exchanges

# [DOCKER_FREQTRADE]
docker compose run --rm freqtrade list-pairs --exchange coinbase --quote USD --print-json

# [DOCKER_FREQTRADE]
docker compose run --rm freqtrade --version
```

## Phase 03b Local Mock Data Parity Checks

These checks are valid in `NO_DOCKER_LOCAL_MODE`.

```powershell
# [LOCAL_VENV]
.\.venv\Scripts\python.exe -m pytest tests\test_data_parity.py

# [LOCAL_VENV]
.\.venv\Scripts\python.exe -m pytest

# [LOCAL_VENV]
.\.venv\Scripts\ruff.exe check .

# [LOCAL_VENV]
.\.venv\Scripts\python.exe scripts\compare_coinbase_data_sources.py

# [HOST_POWERSHELL]
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 no-secrets
```

Local Phase 03b output:

- `src/coinbase_freqtrade_guarded_bot/guard_layer/data_parity.py`;
- `src/coinbase_freqtrade_guarded_bot/network/http_client.py`;
- `tests/test_data_parity.py`;
- `reports/data_parity/2026-06-21_mock_parity_report.md`.

Local Phase 03b validates gate behavior with mock data only. Real Coinbase and Freqtrade/CCXT data parity remains deferred until data access and Docker/Freqtrade runtime checks are available.

## Phase 05 Local Static Strategy Checks

These checks are valid in `NO_DOCKER_LOCAL_MODE`.

```powershell
# [LOCAL_VENV]
.\.venv\Scripts\python.exe -m pytest tests\test_strategy_sanity.py

# [LOCAL_VENV]
.\.venv\Scripts\python.exe -m pytest

# [LOCAL_VENV]
.\.venv\Scripts\ruff.exe check .

# [HOST_POWERSHELL]
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 no-secrets
```

Phase 05 local/static checks parse `user_data/strategies/CoinbaseTrendGuardV1.py` without importing Freqtrade locally. Runtime import, backtest, and dry-run behavior remain `DEFERRED_DOCKER_REQUIRED`.

## Phase 06 Local Offline Backtest Validation Checks

These checks are valid in `NO_DOCKER_LOCAL_MODE`.

```powershell
# [LOCAL_VENV]
.\.venv\Scripts\python.exe -m pytest tests\test_backtest_validation.py

# [LOCAL_VENV]
.\.venv\Scripts\python.exe scripts\run_backtest_report.py

# [LOCAL_VENV]
.\.venv\Scripts\python.exe -m pytest

# [LOCAL_VENV]
.\.venv\Scripts\ruff.exe check .

# [HOST_POWERSHELL]
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 no-secrets
```

Local Phase 06 output:

- `src/coinbase_freqtrade_guarded_bot/research/backtest_validation.py`;
- `tests/test_backtest_validation.py`;
- `scripts/run_backtest_report.py`;
- `reports/backtests/2026-06-21_mock_backtest_report.md`;
- `reports/backtests/2026-06-21_mock_backtest_report.json`.

`LOCAL_OFFLINE_PASS` means:

- deterministic trade-list and equity-curve metric functions pass tests;
- fee/slippage sensitivity returns a numeric scenario table from mock trades;
- Monte Carlo trade-order resampling returns numeric percentiles and probabilities;
- walk-forward output returns numeric mock window results;
- buy-and-hold comparison uses local mock prices;
- markdown and JSON report generation works;
- no network, Docker, credentials, or live trading are required.

`DEFERRED_DOCKER_REQUIRED` still applies to:

- real Freqtrade backtest execution;
- real strategy runtime loading inside Freqtrade;
- Docker-based Freqtrade backtest;
- Docker-based data download;
- real Coinbase/Freqtrade data parity;
- dry-run runtime validation.

## Phase 07 Local Offline Report Bundle

These checks are valid in `NO_DOCKER_LOCAL_MODE`.

```powershell
# [LOCAL_VENV]
.\.venv\Scripts\python.exe scripts\run_backtest_report.py

# [LOCAL_VENV]
.\.venv\Scripts\python.exe -m pytest tests\test_backtest_validation.py

# [LOCAL_VENV]
.\.venv\Scripts\python.exe -m pytest

# [LOCAL_VENV]
.\.venv\Scripts\ruff.exe check .

# [HOST_POWERSHELL]
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 no-secrets
```

Local Phase 07 output:

- `reports/backtests/2026-06-21_strategy_summary.md`;
- `reports/backtests/2026-06-21_trades.csv`;
- `reports/backtests/2026-06-21_metrics.json`;
- `reports/backtests/2026-06-21_drawdown.csv`;
- `reports/backtests/2026-06-21_walkforward.json`;
- `reports/backtests/2026-06-21_montecarlo.json`.

The CSV files are deterministic mock report artifacts and are not real exchange exports. They are safe to regenerate locally with the script above. Phase 07 still does not run Freqtrade, download market data, access credentials, create orders, or validate dry-run runtime behavior.

## Deferred Docker Validation

Status: `DEFERRED_DOCKER_REQUIRED`.

Do not run these commands on the current no-Docker workstation. Run them only in a future Docker-capable environment.

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

Future Docker revalidation must also verify:

- Docker package import smoke test for `coinbase_freqtrade_guarded_bot`;
- Freqtrade strategy import without `sys.path.append`;
- `dry_run=true`;
- no real API keys or secrets;
- no live order path.

## Safety Notes

- Do not run live trading commands.
- Do not paste secrets into chat.
- Configure credentials locally only when a later phase explicitly requires them.
- Coinbase sandbox is not a strategy validation environment.
