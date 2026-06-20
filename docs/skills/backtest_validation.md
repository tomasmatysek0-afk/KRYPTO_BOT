# backtest_validation

## Purpose

Track validation rules for backtests, out-of-sample checks, walk-forward analysis, costs, and baseline comparison.

## Current conclusions

Backtests must account for fees, slippage, data quality, drawdown, out-of-sample behavior, and operational risks.

## Findings

### 2026-06-20 - Bootstrap
Source:
- CODEX_MASTER_PLAN.md

Summary:
No strategy result is acceptable without baseline comparison and realistic validation.

Decision impact:
Backtest implementation is deferred until data parity and baseline strategy phases.

Open questions:
- None for Phase 00.
