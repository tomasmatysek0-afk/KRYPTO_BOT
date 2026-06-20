# Execution Context

## Command Context Labels

Every command in docs, logs, scripts, and responses must use one of:

| Context | Use |
|---|---|
| `[HOST_POWERSHELL]` | Git repository operations, filesystem operations, Docker host commands. |
| `[LOCAL_VENV]` | Local Python package, tests, linting, coverage, CLI. |
| `[DOCKER_APP]` | Future app container commands. |
| `[DOCKER_FREQTRADE]` | Future Freqtrade container commands. |

## Phase 00b Local Commands

```powershell
# [LOCAL_VENV]
python -m pip install --upgrade pip

# [LOCAL_VENV]
python -m pip install -e .

# [LOCAL_VENV]
python -m pytest

# [LOCAL_VENV]
python -m ruff check .

# [LOCAL_VENV]
python -m coinbase_freqtrade_guarded_bot --help
```

## Rule

If the correct context is unclear, stop and write an execution-context blocker instead of guessing.
