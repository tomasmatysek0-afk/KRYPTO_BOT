# backtest_validation

## Purpose

Track validation rules for backtests, out-of-sample checks, walk-forward analysis, costs, and baseline comparison.

## Current conclusions

Backtests must account for fees, slippage, data quality, drawdown, out-of-sample behavior, and operational risks.

## Findings

### 2026-06-21 - Phase 06 local/offline validation
Source:
- CODEX_MASTER_PLAN.md
- `NO_DOCKER_LOCAL_MODE` user constraint
- `src/coinbase_freqtrade_guarded_bot/research/backtest_validation.py`
- `reports/backtests/2026-06-21_mock_backtest_report.md`

Summary:
Phase 06 local work is limited to deterministic offline validation math and report generation. The local report uses mock trades, mock equity points, and mock price series. It does not use Docker, Freqtrade runtime execution, network access, credentials, exchange data downloads, or live trading.

Local checks implemented:
- trade-list metrics: profit, costs, win rate, profit factor, average profit, best/worst trade, max loss streak, and enter_tag aggregation;
- equity-curve metrics: total return, CAGR, drawdown curve, max drawdown, Sharpe, Sortino, and monthly returns;
- fee/slippage sensitivity with a numeric scenario table;
- Monte Carlo trade-order resampling with numeric CAGR/drawdown percentiles and risk probabilities;
- walk-forward report structures with numeric mock window results;
- buy-and-hold comparison from local mock prices;
- markdown and JSON report generation.

Acceptance split:
- `LOCAL_OFFLINE_PASS`: deterministic metric functions and mock report generation can pass locally without Docker, network, credentials, or live trading.
- `DEFERRED_DOCKER_REQUIRED`: real Freqtrade backtest execution, real strategy runtime loading, Docker-based Freqtrade backtest, Docker-based data download, real Coinbase/Freqtrade data parity, and dry-run runtime validation.

Decision impact:
Phase 06 may produce local sample reports, but it must not claim a real strategy backtest, real market-data backtest, real out-of-sample strategy result, or Freqtrade runtime validation has passed.

Open questions:
- None for the local/offline slice. Docker-capable revalidation remains required later.

### 2026-06-20 - Bootstrap
Source:
- CODEX_MASTER_PLAN.md

Summary:
No strategy result is acceptable without baseline comparison and realistic validation.

Decision impact:
Backtest implementation is deferred until data parity and baseline strategy phases.

Open questions:
- None for Phase 00.
