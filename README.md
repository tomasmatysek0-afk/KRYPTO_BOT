# coinbase_freqtrade_guarded_bot

Research, backtesting, dry-run, and controlled validation system for Coinbase spot BTC/ETH strategies.

## MVP Scope

- Spot only.
- Long only.
- BTC and ETH only.
- Backtest and dry-run only.
- No live trading support in MVP.
- No futures, leverage, shorts, options, perpetuals, margin, lending, or staking in the trading engine.
- Coinbase sandbox is not considered a strategy validation environment.

## Safety

This repository must never contain real Coinbase API keys, private keys, seed phrases, session cookies, key exports, `.env` files, databases, cache folders, or runtime artifacts.

Live order creation is outside the MVP and is blocked unless a later explicit live pilot approval phase is completed.

## Disclaimer

This project is a tool for research and auditable testing of trading strategies, not investment advice or a promise of profit. Historical backtest and dry-run results are not a guarantee of future results. Cryptocurrency trading is risky and may lead to loss of part or all invested capital. Tax information in this project is a technical basis for recordkeeping, not tax advice. For final tax filing, current rules must be verified and a tax advisor should be consulted.
