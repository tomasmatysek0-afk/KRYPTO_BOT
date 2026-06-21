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
