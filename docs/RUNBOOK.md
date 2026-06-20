# Runbook

## Command Contexts

Every command must be marked with one execution context.

| Context | Use |
|---|---|
| `[HOST_POWERSHELL]` | Git repository operations, folders, Docker commands on Windows host. |
| `[LOCAL_VENV]` | Local Python package commands, pytest, ruff, mypy, CLI app commands. |
| `[DOCKER_APP]` | Future app container commands. |
| `[DOCKER_FREQTRADE]` | Future Freqtrade container commands. |

## Phase 00 Commands

```powershell
# [HOST_POWERSHELL]
git status --short --branch

# [HOST_POWERSHELL]
git remote -v

# [HOST_POWERSHELL]
git diff --stat
```

## Safety Notes

- Do not run live trading commands.
- Do not paste secrets into chat.
- Configure credentials locally only when a later phase explicitly requires them.
- Coinbase sandbox is not a strategy validation environment.

## Future Command Catalog

Phase 00b will add `scripts/dev.ps1` as the Windows-first command entry point.
