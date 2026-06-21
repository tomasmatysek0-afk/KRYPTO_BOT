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

## Phase 05b Minimal Guard Core

The minimal guard core evaluates order intents before backtest/dry-run expansion.

Implemented local rules:

- typed `OrderIntent` and `RiskDecision` models;
- file/env kill-switch blocks intents;
- `ALLOW_LIVE_TRADING=false` equivalent behavior through `allow_live_trading=False`;
- live intents are rejected by default;
- leverage is rejected;
- opening shorts is rejected;
- non-spot modes are rejected by model/type constraints;
- stake above configured maximum is rejected;
- open intent count at or above configured maximum is rejected;
- every decision, including rejection, is written to append-only JSONL audit.

The minimal guard core does not create live orders, Coinbase previews, reconciliation, or UI toggles.
