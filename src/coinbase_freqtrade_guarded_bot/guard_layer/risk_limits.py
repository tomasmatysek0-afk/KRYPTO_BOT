"""Minimal fail-closed risk limit evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from coinbase_freqtrade_guarded_bot.guard_layer.audit_writer import AuditWriter
from coinbase_freqtrade_guarded_bot.guard_layer.kill_switch import is_kill_switch_active
from coinbase_freqtrade_guarded_bot.guard_layer.order_intent import OrderIntent, RiskDecision


@dataclass(frozen=True, slots=True)
class RiskLimits:
    """Basic risk limits for the MVRS guard core."""

    max_stake_per_intent: Decimal
    max_open_intents: int
    allow_live_trading: bool = False

    def __post_init__(self) -> None:
        if self.max_stake_per_intent <= 0:
            raise ValueError("max_stake_per_intent must be positive.")
        if self.max_open_intents < 0:
            raise ValueError("max_open_intents must not be negative.")


def evaluate_intent(
    intent: OrderIntent,
    limits: RiskLimits,
    *,
    open_intent_count: int,
    kill_switch_active: bool = False,
) -> RiskDecision:
    """Evaluate an intent against minimal fail-closed risk limits."""
    if kill_switch_active:
        return RiskDecision.reject(
            intent,
            "kill_switch_active",
            "Kill-switch is active.",
        )
    if not intent.dry_run and not limits.allow_live_trading:
        return RiskDecision.reject(
            intent,
            "live_trading_disabled",
            "Live execution path is disabled in MVP.",
        )
    if intent.trading_mode != "spot":
        return RiskDecision.reject(intent, "non_spot_rejected", "Only spot trading is allowed.")
    if intent.leverage != Decimal("1"):
        return RiskDecision.reject(intent, "leverage_rejected", "Leverage is forbidden.")
    if intent.side == "sell" and intent.position_effect == "open":
        return RiskDecision.reject(intent, "short_rejected", "Opening shorts is forbidden.")
    if intent.stake_amount > limits.max_stake_per_intent:
        return RiskDecision.reject(
            intent,
            "stake_limit_exceeded",
            "Intent stake is above max_stake_per_intent.",
        )
    if open_intent_count >= limits.max_open_intents:
        return RiskDecision.reject(
            intent,
            "open_intent_limit_exceeded",
            "Open intent count is at or above max_open_intents.",
        )
    return RiskDecision.approve(intent)


def evaluate_and_audit_intent(
    intent: OrderIntent,
    limits: RiskLimits,
    audit_writer: AuditWriter,
    *,
    open_intent_count: int,
    kill_switch_path: Path,
) -> RiskDecision:
    """Evaluate an intent, append the decision to audit, and return the decision."""
    decision = evaluate_intent(
        intent,
        limits,
        open_intent_count=open_intent_count,
        kill_switch_active=is_kill_switch_active(path=kill_switch_path),
    )
    audit_writer.write_decision(intent, decision)
    return decision
