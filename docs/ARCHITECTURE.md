# Architecture

## Purpose

This project is a safe research and dry-run system for Coinbase spot BTC/ETH strategy validation.

## Current Phase 00 Architecture

The repository starts with governance, audit, and policy files before application logic. Custom Python code will later live under `src/coinbase_freqtrade_guarded_bot/`.

## Target Flow

```text
data
-> data validation
-> baseline strategy
-> backtest
-> dry-run
-> guard layer
-> audit
-> tax ledger
-> manual approval workflow
```

Live order execution is not part of the MVP.

## Component Boundaries

- `src/coinbase_freqtrade_guarded_bot/`: future importable application package.
- `user_data/`: future Freqtrade runtime convention folder.
- `docs/`: governance, architecture, policies, ADRs, and skills.
- `reports/`: generated research, data parity, backtest, dry-run, audit, and tax outputs.
- `ui/`: future local read-only dashboard.

## Safety Defaults

- Fail closed when uncertain.
- Do not trade when audit, reconciliation, data quality, or kill-switch state is unknown.
- No Coinbase sandbox result is accepted as strategy validation.

## Phase 05 Baseline Strategy

`user_data/strategies/CoinbaseTrendGuardV1.py` is the local/static baseline strategy skeleton.

Design constraints:

- Freqtrade strategy file, not application package business logic.
- Long-only.
- Spot only.
- Main timeframe: 4h.
- Informative trend timeframe: 1d.
- BTC/USD and ETH/USD only through config.
- No direct Coinbase, CCXT, HTTP, or order client code inside the strategy.
- No `sys.path` import hacks.
- Runtime Freqtrade import/backtest validation is deferred until Docker is available.
