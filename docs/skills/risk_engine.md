# risk_engine

## Purpose

Track risk engine rules, guard decisions, and kill-switch behavior.

## Current conclusions

Risk must fail closed. No live execution is allowed in MVP.

## Findings

### 2026-06-20 - Bootstrap
Source:
- CODEX_MASTER_PLAN.md

Summary:
The risk policy bans live trading, leverage, futures, shorts, and secrets. Guard implementation starts later.

Decision impact:
Phase 00 documents hard limits before any strategy or execution code exists.

Open questions:
- None for Phase 00.
