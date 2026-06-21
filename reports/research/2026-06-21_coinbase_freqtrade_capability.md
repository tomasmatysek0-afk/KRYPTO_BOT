# Coinbase/Freqtrade Capability Research - 2026-06-21

## Question

Can this project rely on Freqtrade/CCXT for Coinbase spot BTC/ETH data and dry-run research in the current phase?

## Sources

- Freqtrade repository supported exchange list: https://github.com/freqtrade/freqtrade
- Freqtrade exchange-specific notes: https://www.freqtrade.io/en/stable/exchanges/
- Freqtrade utility subcommands: https://www.freqtrade.io/en/stable/utils/
- Freqtrade issue #9606, Coinbase Advanced Trade integration: https://github.com/freqtrade/freqtrade/issues/9606
- CCXT Coinbase exchange docs: https://docs.ccxt.com/docs/exchanges/coinbase
- CCXT manual: https://github.com/ccxt/ccxt/wiki/manual
- Coinbase Advanced Trade list products: https://docs.cdp.coinbase.com/api-reference/advanced-trade-api/rest-api/products/list-products
- Coinbase Advanced Trade product candles: https://docs.cdp.coinbase.com/api-reference/advanced-trade-api/rest-api/products/get-product-candles
- Coinbase Advanced Trade public product candles: https://coinbase-cloud.mintlify.app/api-reference/advanced-trade-api/rest-api/public/get-public-product-candles
- Coinbase Exchange product candles: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/products/get-product-candles

## Summary

CCXT currently documents a `coinbase` exchange with `fetchMarkets`, `fetchOHLCV`, `fetchTrades`, `fetchOrderBook`, and other unified methods. CCXT also documents `fetchOHLCV` for Coinbase as returning candles ordered as timestamp, open, high, low, close, and volume.

Freqtrade's public supported spot exchange list does not explicitly list Coinbase as a guaranteed supported exchange. It says other exchanges may potentially work, but without a guarantee. A Freqtrade issue specifically asking about Coinbase Advanced Trade integration was closed as not planned and labeled as unsupported exchange / CCXT-related.

Coinbase Advanced Trade product examples use dash product IDs such as `BTC-USD`. Freqtrade/CCXT strategy configuration normally uses slash pair symbols such as `BTC/USD`. This project must explicitly validate that mapping.

Coinbase Advanced Trade candle docs include the project-required `FOUR_HOUR` and `ONE_DAY` granularities. The public candle docs state a default/max of 350 candle buckets. The older Coinbase Exchange candle endpoint documents a 300-candle maximum and does not include 4h granularity. For this project, Coinbase Advanced Trade is the better direct candle candidate.

## Risks

- Freqtrade may not treat Coinbase as a supported/validated exchange even if CCXT exposes a Coinbase class.
- Local Docker commands cannot be run in `NO_DOCKER_LOCAL_MODE`, so `list-exchanges`, `list-pairs`, and container import checks remain unproven.
- Pair mapping may differ between Coinbase product IDs and Freqtrade/CCXT pair symbols.
- Candle limits require deterministic pagination for backtests.
- Timestamp semantics must be verified before using 4h/1d candles.
- Coinbase candle volume semantics must be verified before volume-based indicators or reports rely on it.
- Order book support has a reported concern in a Freqtrade Coinbase Advanced issue and must be tested before any dry-run workflow relies on order-book pricing.

## Recommendation

Use state `PARTIAL_RESEARCH_DOCKER_DEFERRED`.

Do not mark Freqtrade/Coinbase as PASS yet. Continue safe local work with mocked/offline data logic and documentation.

For Phase 03b, design the Data Parity Gate around Coinbase Advanced Trade as the candidate authoritative source, with Freqtrade/CCXT treated as a candidate engine/data adapter until verified.

On a future Docker-capable machine, run:

```powershell
# [DOCKER_FREQTRADE]
docker compose run --rm freqtrade list-exchanges

# [DOCKER_FREQTRADE]
docker compose run --rm freqtrade list-pairs --exchange coinbase --quote USD --print-json

# [DOCKER_FREQTRADE]
docker compose run --rm freqtrade --version
```

Then compare runtime results against the Coinbase Advanced Trade product/candle endpoints before proceeding to strategy validation.

## What Not To Implement

- Do not use live trading.
- Do not use real API keys or private endpoints for this research phase.
- Do not use Coinbase sandbox as validation data.
- Do not assume `coinbasepro` is correct for Advanced Trade.
- Do not use 4h data without validating candle closure and timestamp alignment.
- Do not use unpaginated Coinbase candles for historical backtests.
- Do not expand beyond BTC/USD and ETH/USD.

## Impact On The Project

Phase 03 cannot be fully passed locally because Docker/Freqtrade runtime checks are unavailable. The safe local result is enough to continue with documentation and offline Data Parity Gate design, but not enough for live readiness or real dry-run runtime claims.

The current Phase 02 config pair notation `BTC/USD` and `ETH/USD` is still a reasonable Freqtrade/CCXT candidate, but it must map cleanly to Coinbase product IDs `BTC-USD` and `ETH-USD` in Phase 03b.
