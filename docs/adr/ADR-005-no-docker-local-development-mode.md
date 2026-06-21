# ADR-005 - NO_DOCKER_LOCAL_MODE local development

## Status

Accepted - 2026-06-21

## Context

The local workstation cannot run Docker-dependent project checks at this time:

- Docker Desktop is not available.
- Docker Compose is not available.
- WSL2 is not installed.
- The operator does not have administrator rights.
- `winget` cannot install Docker because the source fails with `0x8a15000f : Data required by the source is missing`.
- `winget source reset --force` requires administrator privileges.

The project still needs to continue in safe, restartable slices. Stopping all work until Docker is available would block local progress on Python package code, tests, documentation, guard logic, audit logic, risk rules, tax records, reports, and mocked/offline data logic.

## Decision

The project will continue locally in `NO_DOCKER_LOCAL_MODE`.

Docker remains part of the target architecture. Docker-related files may be created and maintained, but Docker runtime behavior is not locally validated until the project is transferred to a Docker-capable environment.

Docker-dependent acceptance criteria are marked `DEFERRED_DOCKER_REQUIRED`. They are not passed. They remain mandatory before live-pilot readiness.

## Consequences

Positive consequences:

- Local development can continue without administrator privileges.
- Python package, CLI, local tests, guard, audit, risk, tax, reporting, and documentation work remain unblocked.
- The repository stays portable for a future Docker-capable machine.

Tradeoffs:

- Docker Compose validation cannot be completed locally.
- Freqtrade container execution cannot be completed locally.
- Docker import smoke tests cannot be completed locally.
- Docker dry-run cannot be completed locally.

The project must not claim Docker readiness until those checks pass on a Docker-capable machine.

## Deferred Docker acceptance criteria

These criteria are deferred and must be revalidated later:

- Docker Compose config validation.
- Freqtrade container startup.
- Freqtrade `--help` in the container.
- Docker package import smoke test for `coinbase_freqtrade_guarded_bot`.
- Freqtrade strategy import smoke test without `sys.path.append`.
- Docker/Freqtrade backtest execution.
- Docker/Freqtrade dry-run execution.
- Verification that Freqtrade config remains `dry_run=true`.

## Future Docker revalidation checklist

When Docker is available, run a dedicated revalidation slice:

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

Then verify:

- the package imports inside the Freqtrade container;
- Freqtrade strategies do not use `sys.path.append`;
- Docker config contains no real API keys or secrets;
- live trading remains disabled;
- dry-run mode remains enabled;
- `LOG.md` and `PROJECT_STATE.md` record PASS, FAIL, or remaining blockers.

## Portability requirements

- Application logic must not hardcode Windows-only absolute paths.
- Application logic must not depend on the current user's profile directory.
- Repository paths in config and docs should be relative where possible.
- Docker and Freqtrade files must stay aligned with the package import policy.
- Unit tests must remain offline by default.
- Generated runtime data, caches, exports, local databases, and secrets must not be committed.

## Safety constraints

- No live trading in MVP.
- No real API keys.
- No secrets.
- No leverage.
- No futures.
- No shorts.
- Spot BTC/ETH only.
- Docker deferral must not weaken guard, audit, kill-switch, or no-live-execution requirements.
