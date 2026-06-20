# Packaging

## Package Layout

Application code lives in:

```text
src/coinbase_freqtrade_guarded_bot/
```

Freqtrade runtime files live under `user_data/` and may import validated helpers from the package once Docker import policy is configured.

## Build Backend

Phase 00b uses `hatchling` as the default build backend from the master plan. It is a build/dev dependency only.

## Runtime Dependencies

Phase 00b has no runtime dependencies beyond the Python standard library.

## Dev Dependencies

The bootstrap dev stack is limited to:

- `hatchling`;
- `pytest`;
- `pytest-cov`;
- `pytest-socket`;
- `ruff`.

These are allowed by CODEX_MASTER_PLAN.md for Phase 00b and are locked in `requirements-dev.lock`.

## CLI

The package exposes only safe placeholder commands:

- `cbot-data-parity`;
- `cbot-backtest-report`;
- `cbot-dryrun-healthcheck`;
- `cbot-tax-export`.

No live trading command is present in MVP.

## Locking

- `requirements.lock` records runtime dependencies.
- `requirements-dev.lock` records exact dev environment pins.
- `constraints.txt` mirrors locked dev constraints for reproducible installs.
