# Risk Policy

## MVP Bans

- No live trading with real money.
- No real API keys or secrets in the repository.
- No futures.
- No leverage.
- No shorts.
- No options, perpetuals, margin, lending, or staking in the trading engine.
- No altcoins in the first version.
- No live order path in MVP.
- No claim of guaranteed profit.

## Required MVP Scope

- Spot only.
- Long only.
- BTC and ETH only.
- Backtest and dry-run / simulation only.
- Main timeframe: 4h.
- Trend filter: 1d.
- Every trade proposal must have an audit record.

## Coinbase Sandbox

Coinbase sandbox is not suitable for strategy validation. It may help with API shape checks later, but it must not be used as evidence that a strategy works.

## Fail-Closed Rules

Trading is not possible when:

- the kill-switch is active or unreadable;
- audit writing is unavailable;
- reconciliation is unknown;
- data parity fails without a safe fallback;
- live trading is requested before Phase 18 approval.
