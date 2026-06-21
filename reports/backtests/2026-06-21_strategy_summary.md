# Offline Backtest Validation Report

Strategy: `CoinbaseTrendGuardV1`
Config version: `phase-06-local-offline-sample`
Generated at: `2026-06-21T13:16:00+00:00`
Pairs: `BTC/USD, ETH/USD`
Timeframe: `1h with 1d trend context`
Fee model: mock roundtrip fee scenarios only; no exchange execution
Slippage model: mock local slippage scenarios only; no exchange execution
Data source decision: ADR-002 provisional: Coinbase Advanced Trade candidate raw source; Freqtrade engine candidate pending real parity and Docker checks.
Local acceptance: `LOCAL_OFFLINE_PASS`
Deferred runtime status: `DEFERRED_DOCKER_REQUIRED`
Conclusion: `RESEARCH_ONLY`

## Core Metrics

- Total profit: $218.05
- CAGR: 75.48%
- Max drawdown: 0.84%
- Sharpe: 5.1054
- Sortino: 13.3796
- Profit factor: 2.9596
- Win rate: 66.67%
- Average profit/trade: $36.34
- Number of trades: 6
- Exposure: 42.86%
- Max loss streak: 1
- Best trade: $174.06
- Worst trade: $-84.92
- Buy-and-hold total return: 7.18%

## Fee And Slippage Sensitivity

| Scenario | Fee rate | Slippage rate | Total profit | Total return | Win rate |
|---|---:|---:|---:|---:|---:|
| base_fee | 0.10% | 0.05% | $214.12 | 2.14% | 66.67% |
| worst_fee | 0.30% | 0.05% | $179.62 | 1.80% | 66.67% |
| slippage_low | 0.10% | 0.05% | $214.12 | 2.14% | 66.67% |
| slippage_medium | 0.10% | 0.15% | $196.88 | 1.97% | 66.67% |
| slippage_high | 0.10% | 0.30% | $171.00 | 1.71% | 66.67% |

## Monte Carlo

- Simulations: 250
- 5/50/95 percentile CAGR: 75.48% / 75.48% / 75.48%
- 5/50/95 percentile max drawdown: 0.82% / 0.85% / 1.11%
- Worst simulated drawdown: 1.11%
- Probability drawdown above limit: 0.00%
- Probability negative result after costs: 0.00%

## Walk Forward

- Windows: 3
- Train/test window days: 14 / 5
- Profitable/loss windows: 2 / 1
- Aggregated profit: $218.05
- Aggregated max drawdown: 0.84%
- Walk-forward conclusion: `PASS`

## Enter Tag Aggregation

- `trend_pullback`: trades=4, total_profit=$22.49
- `volume_confirmed`: trades=2, total_profit=$195.56

## Monthly Returns

- 2026-01: 2.18%

## Deferred Runtime Items

- `DEFERRED_DOCKER_REQUIRED`: real Freqtrade backtest execution
- `DEFERRED_DOCKER_REQUIRED`: real strategy runtime loading inside Freqtrade
- `DEFERRED_DOCKER_REQUIRED`: Docker-based Freqtrade backtest
- `DEFERRED_DOCKER_REQUIRED`: Docker-based data download
- `DEFERRED_DOCKER_REQUIRED`: real Coinbase/Freqtrade data parity
- `DEFERRED_DOCKER_REQUIRED`: dry-run runtime validation

## Disclaimer

Research-only offline sample report. This is not financial advice, not a profit guarantee, and not evidence that real Freqtrade backtesting or dry-run runtime validation has passed.
