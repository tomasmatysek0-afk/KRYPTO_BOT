# ADR-002 - Provisional data source policy

## Status

Accepted provisionally - 2026-06-21.

Final production/dry-run validation status: `REAL_DATA_PARITY_DEFERRED`.

## Context

The project needs an auditable data source policy before baseline strategy work can be trusted.

Phase 03 found:

- CCXT documents Coinbase market and OHLCV methods.
- Freqtrade does not list Coinbase as a guaranteed supported spot exchange.
- A Freqtrade Coinbase Advanced Trade issue was closed as not planned and labeled unsupported exchange / CCXT-related.
- Coinbase Advanced Trade product IDs use dash notation such as `BTC-USD`.
- Freqtrade/CCXT pair candidates use slash notation such as `BTC/USD`.

Phase 03b implemented a local mocked/offline Data Parity Gate:

- pair mapping rules;
- closed-candle comparison;
- UTC timestamp normalization;
- missing/shifted/duplicate candle failures;
- OHLC and volume tolerance behavior;
- deterministic 1h to 4h aggregation;
- markdown parity reports;
- bounded HTTP retry primitives.

Current local mode is `NO_DOCKER_LOCAL_MODE`, so Docker/Freqtrade runtime checks and real source parity remain deferred.

## Decision

For continued local development, Coinbase Advanced Trade is the candidate authoritative raw candle source, and Freqtrade remains the candidate research/backtest/dry-run engine.

This is a provisional decision, not proof of real data parity.

Final data-source acceptance requires:

- real Coinbase Advanced Trade BTC/USD and ETH/USD product/candle checks;
- real Freqtrade/CCXT Coinbase pair checks;
- real comparison of closed 1h, 4h, and 1d candles;
- Docker/Freqtrade `list-exchanges`, `list-pairs`, and version checks when Docker is available.

## Consequences

Local work may continue on:

- offline data parity logic;
- mocked tests;
- guard and audit logic;
- report generation;
- data downloader design;
- conversion design from Coinbase Advanced Trade candles into Freqtrade-compatible data.

Local work must not claim:

- Freqtrade sees Coinbase at runtime;
- BTC/USD and ETH/USD are available in Freqtrade at runtime;
- Coinbase and Freqtrade candles match;
- dry-run has been validated;
- live readiness exists.

## Data Failure Behavior

The system fails closed when data quality is unclear.

If real data parity later fails:

- do not use the failing data for strategy validation;
- write a parity report;
- mark the affected phase BLOCKED or PARTIAL according to scope;
- prefer Coinbase Advanced Trade as the candidate authoritative data source;
- use Freqtrade only as an engine after data conversion and successful parity checks;
- do not continue to live readiness.

If data is unavailable:

- do not interpolate missing candles;
- do not invent prices or volume;
- do not backfill from non-authoritative sources without a new ADR;
- continue only with mocked/offline tests and documentation.

## Risks

- Coinbase Advanced Trade candle limits require pagination.
- Coinbase product IDs must be mapped to Freqtrade/CCXT pair notation.
- Timestamp bucket semantics must be verified on real data.
- Volume semantics must be verified before volume filters rely on them.
- Freqtrade runtime support for Coinbase remains unproven.
- Docker runtime validation remains unavailable locally.

## Required Future Checks

```powershell
# [DOCKER_FREQTRADE]
docker compose run --rm freqtrade list-exchanges

# [DOCKER_FREQTRADE]
docker compose run --rm freqtrade list-pairs --exchange coinbase --quote USD --print-json

# [DOCKER_FREQTRADE]
docker compose run --rm freqtrade --version
```

Also required:

- real Coinbase Advanced Trade candle download for BTC-USD and ETH-USD;
- real parity report for closed 1h, 4h, and 1d candles;
- no real API keys or secrets in repository files;
- no live trading or live orders.
