# freqtrade_coinbase_ccxt

## Purpose

Track verified knowledge about Freqtrade, CCXT, Coinbase support, pair naming, OHLCV behavior, and data limitations.

## Current conclusions

Phase 03 local research result: `PARTIAL_RESEARCH_DOCKER_DEFERRED`.

CCXT documents a `coinbase` exchange with market and OHLCV methods, but Freqtrade does not list Coinbase as a guaranteed supported spot exchange. Freqtrade runtime checks must run later in a Docker-capable environment before this project treats Freqtrade Coinbase support as PASS.

Coinbase Advanced Trade product IDs use dash notation such as `BTC-USD`; Freqtrade/CCXT configs use slash notation candidates such as `BTC/USD`. This mapping must be tested in the Data Parity Gate.

Coinbase Advanced Trade candle docs include `FOUR_HOUR` and `ONE_DAY`, which match the project 4h main timeframe and 1d trend filter. Candle limits require deterministic pagination and closed-candle validation.

## Findings

### 2026-06-20 - Bootstrap
Source:
- CODEX_MASTER_PLAN.md

Summary:
Freqtrade is planned as research/backtest/dry-run engine. Coinbase data quality must be checked before strategy validation.

Decision impact:
Phase 03 must produce a research report before data-source decisions.

Open questions:
- Does current Freqtrade/CCXT support Coinbase pairs and OHLCV adequately?

### 2026-06-21 - Phase 03 local research

Sources:
- https://github.com/freqtrade/freqtrade
- https://www.freqtrade.io/en/stable/exchanges/
- https://www.freqtrade.io/en/stable/utils/
- https://github.com/freqtrade/freqtrade/issues/9606
- https://docs.ccxt.com/docs/exchanges/coinbase
- https://github.com/ccxt/ccxt/wiki/manual
- https://docs.cdp.coinbase.com/api-reference/advanced-trade-api/rest-api/products/list-products
- https://docs.cdp.coinbase.com/api-reference/advanced-trade-api/rest-api/products/get-product-candles
- https://coinbase-cloud.mintlify.app/api-reference/advanced-trade-api/rest-api/public/get-public-product-candles
- https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/products/get-product-candles

Findings:
- CCXT has a documented `coinbase` exchange and documents `fetchOHLCV`.
- Freqtrade's guaranteed supported spot exchange list does not include Coinbase.
- Freqtrade issue #9606 about Coinbase Advanced Trade was closed as not planned and labeled unsupported exchange / CCXT-related.
- Coinbase Advanced Trade examples use product IDs like `BTC-USD`.
- Coinbase Advanced Trade candles support `FOUR_HOUR` and `ONE_DAY`; the public candle docs state default/max 350 candle buckets.
- Older Coinbase Exchange candles document a 300-candle maximum and do not include 4h granularity.

Decision impact:
- Treat Freqtrade Coinbase as unverified until Docker runtime checks pass.
- Use Coinbase Advanced Trade as the candidate authoritative data source if Freqtrade/CCXT parity is not proven.
- Phase 03b must explicitly validate pair mapping, candle timestamps, closed candle handling, pagination, and volume semantics.

Open questions:
- Will `[DOCKER_FREQTRADE] docker compose run --rm freqtrade list-exchanges` include Coinbase in the future Docker-capable environment?
- Will `[DOCKER_FREQTRADE] docker compose run --rm freqtrade list-pairs --exchange coinbase --quote USD --print-json` show active BTC/USD and ETH/USD?
- Does Freqtrade's Coinbase order book path work well enough for dry-run pricing, or should dry-run avoid order-book-dependent assumptions?
