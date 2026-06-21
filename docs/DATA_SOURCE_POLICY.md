# Data Source Policy

## Status

Phase 04 provisional ADR result - 2026-06-21.

Current mode: `NO_DOCKER_LOCAL_MODE`.

Docker/Freqtrade runtime checks are `DEFERRED_DOCKER_REQUIRED`, not passed.

Current ADR: `docs/adr/ADR-002-data-source-policy.md`.

## Scope

This policy controls market data selection for the Coinbase spot BTC/ETH research system.

Hard limits remain unchanged:

- no live trading in MVP;
- no real API keys or secrets;
- no futures;
- no leverage;
- no shorts;
- spot BTC/ETH only;
- fail closed when data quality is unclear.

## Current Findings

CCXT documents a `coinbase` exchange class with market, ticker, order book, trade, and OHLCV methods, including `fetchMarkets` and `fetchOHLCV`.

Freqtrade uses CCXT and may be able to access exchanges beyond its explicitly tested set, but its current public supported spot exchange list does not list Coinbase as a guaranteed supported exchange. The Freqtrade project states that other exchanges may work, but are not guaranteed.

A Freqtrade GitHub issue about Coinbase Advanced Trade integration was closed as not planned and labeled as an unsupported exchange / CCXT-related question. This means Freqtrade+Coinbase must be treated as unverified until Docker runtime checks prove otherwise.

Coinbase Advanced Trade product identifiers use dash format, for example `BTC-USD`. Freqtrade/CCXT pair notation is expected to use slash format, for example `BTC/USD`. The mapping must be tested before any backtest or dry-run output is trusted.

## Pair Mapping

| Project pair | Coinbase product id | Base | Quote | Status |
|---|---|---|---|---|
| `BTC/USD` | `BTC-USD` | BTC | USD | Candidate, requires runtime validation |
| `ETH/USD` | `ETH-USD` | ETH | USD | Candidate, requires runtime validation |

The project must not add USDC, USDT, EUR, altcoins, futures, or perpetual products in MVRS.

## Candle Data Candidate

Coinbase Advanced Trade candles are the preferred candidate for authoritative raw market data if Freqtrade/CCXT parity is not proven.

Reasons:

- Coinbase Advanced Trade documents direct candle granularities including `FOUR_HOUR` and `ONE_DAY`.
- The main project timeframe is 4h and the trend filter is 1d.
- Public/market candle responses contain timestamp, open, high, low, close, and volume fields.

Known constraints:

- the candle endpoint is bounded to a limited number of buckets per request;
- longer backtest ranges require deterministic pagination;
- candle ordering, close-time handling, timestamp alignment, and volume semantics must be validated before use;
- only closed candles may be used for strategy decisions and backtests.

## Provisional Decision

State: `PROVISIONAL_ADR_ACCEPTED_REAL_DATA_DEFERRED`.

Do not treat Freqtrade Coinbase support as proven yet.

For continued local development, Coinbase Advanced Trade is the candidate authoritative raw candle source, and Freqtrade remains the candidate research/backtest/dry-run engine. This is not a real-data parity PASS.

Proceed locally with:

- documentation;
- mocked/offline data logic;
- pair mapping tests;
- data quality and parity test design;
- deterministic pagination design;
- local reports.

Defer until Docker is available:

- `[DOCKER_FREQTRADE] docker compose run --rm freqtrade list-exchanges`;
- `[DOCKER_FREQTRADE] docker compose run --rm freqtrade list-pairs --exchange coinbase --quote USD --print-json`;
- `[DOCKER_FREQTRADE] docker compose run --rm freqtrade --version`;
- Docker import smoke test for `coinbase_freqtrade_guarded_bot`;
- Freqtrade strategy import smoke test;
- any Freqtrade download/backtest/dry-run runtime command.

## Data Parity Gate Requirements

Before strategy validation, Phase 03b must compare candidate data sources for:

- pair availability for BTC/USD and ETH/USD;
- mapping between `BTC/USD` and `BTC-USD`, and between `ETH/USD` and `ETH-USD`;
- 4h and 1d candle availability;
- timestamp timezone and bucket start/end semantics;
- ordering and duplicate candles;
- missing candles and gaps;
- OHLC consistency;
- volume definition and numeric precision;
- fetch limits and pagination behavior;
- closed-candle-only handling.

If Freqtrade/CCXT Coinbase data differs materially from Coinbase Advanced Trade data, prefer Coinbase Advanced Trade as authoritative data and use Freqtrade as the research/backtest engine only after conversion and parity checks.

## Phase 03b Local Gate Implementation

Local status: `LOCAL_MOCK_DONE_REAL_DATA_DEFERRED`.

The project now has deterministic offline parity primitives in `src/coinbase_freqtrade_guarded_bot/guard_layer/data_parity.py`.

Implemented local behavior:

- only BTC/USD and ETH/USD are accepted;
- Coinbase product mapping is explicit: `BTC/USD` -> `BTC-USD`, `ETH/USD` -> `ETH-USD`;
- only 1h, 4h, and 1d timeframes are accepted;
- all candle timestamps are normalized to UTC;
- unclosed candles are ignored before comparison;
- missing candles fail;
- shifted timestamps fail;
- duplicate timestamps fail;
- OHLC differences above configured tolerance fail;
- volume differences can warn or fail according to config;
- 1h candles can be deterministically aggregated to complete 4h candles;
- incomplete 4h groups are not interpolated;
- markdown reports can be rendered and written.

The network layer now has an injected-transport HTTP client with deterministic tests for:

- HTTP 429 retry handling;
- `Retry-After` handling;
- HTTP 503 retry handling;
- timeout retry handling;
- retry exhaustion.

Still deferred:

- real Coinbase Advanced Trade data download;
- Freqtrade/CCXT data download;
- Docker/Freqtrade `list-exchanges`, `list-pairs`, and version checks;
- real data parity report using live market data.

## Phase 04 Provisional ADR

ADR-002 records a provisional local decision:

- Coinbase Advanced Trade is the candidate authoritative raw candle source.
- Freqtrade remains the candidate research/backtest/dry-run engine.
- Final data-source acceptance is blocked until real data parity and Docker/Freqtrade runtime checks run.
- If real Freqtrade/CCXT data mismatches Coinbase Advanced Trade, prefer Coinbase Advanced Trade data and convert it to Freqtrade-compatible format.
- If data quality is unclear, fail closed.

## Do Not Implement

- Do not use Coinbase sandbox as a strategy validation source.
- Do not use private endpoints, credentials, or API keys for Phase 03 research.
- Do not mark Freqtrade Coinbase support as PASS without runtime checks.
- Do not trade or generate live orders.
- Do not expand beyond BTC/USD and ETH/USD.
- Do not use unpaginated candle calls for historical backtests.
- Do not use open/incomplete candles for backtest decisions.
