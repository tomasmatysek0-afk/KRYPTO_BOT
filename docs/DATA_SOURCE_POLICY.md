# Data Source Policy

## Status

Phase 03 local research result - 2026-06-21.

Current mode: `NO_DOCKER_LOCAL_MODE`.

Docker/Freqtrade runtime checks are `DEFERRED_DOCKER_REQUIRED`, not passed.

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

State: `PARTIAL_RESEARCH_DOCKER_DEFERRED`.

Do not treat Freqtrade Coinbase support as proven yet.

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

## Do Not Implement

- Do not use Coinbase sandbox as a strategy validation source.
- Do not use private endpoints, credentials, or API keys for Phase 03 research.
- Do not mark Freqtrade Coinbase support as PASS without runtime checks.
- Do not trade or generate live orders.
- Do not expand beyond BTC/USD and ETH/USD.
- Do not use unpaginated candle calls for historical backtests.
- Do not use open/incomplete candles for backtest decisions.
