"""Tests for minimal risk limit evaluation."""

from __future__ import annotations

from decimal import Decimal

import pytest

from coinbase_freqtrade_guarded_bot.guard_layer.order_intent import OrderIntent
from coinbase_freqtrade_guarded_bot.guard_layer.risk_limits import RiskLimits, evaluate_intent


def _intent(**overrides: object) -> OrderIntent:
    values = {
        "intent_id": "intent-1",
        "pair": "BTC/USD",
        "side": "buy",
        "position_effect": "open",
        "stake_amount": Decimal("100"),
    }
    values.update(overrides)
    return OrderIntent(**values)  # type: ignore[arg-type]


def _limits(**overrides: object) -> RiskLimits:
    values = {
        "max_stake_per_intent": Decimal("250"),
        "max_open_intents": 2,
        "allow_live_trading": False,
    }
    values.update(overrides)
    return RiskLimits(**values)  # type: ignore[arg-type]


def test_risk_limits_approve_safe_dry_run_intent() -> None:
    """A safe dry-run spot long intent is approved."""
    decision = evaluate_intent(_intent(), _limits(), open_intent_count=0)

    assert decision.approved
    assert decision.reason_code == "approved"


@pytest.mark.parametrize(
    ("intent", "reason_code"),
    [
        (_intent(dry_run=False), "live_trading_disabled"),
        (_intent(trading_mode="futures"), "non_spot_rejected"),
        (_intent(trading_mode="spot", leverage=Decimal("2")), "leverage_rejected"),
        (_intent(side="sell", position_effect="open"), "short_rejected"),
        (_intent(stake_amount=Decimal("251")), "stake_limit_exceeded"),
    ],
)
def test_risk_limits_reject_forbidden_intents(intent: OrderIntent, reason_code: str) -> None:
    """Forbidden intent properties fail closed."""
    decision = evaluate_intent(intent, _limits(), open_intent_count=0)

    assert not decision.approved
    assert decision.reason_code == reason_code


def test_risk_limits_reject_kill_switch_and_open_intent_limit() -> None:
    """Kill-switch and open intent count limit both block intents."""
    kill_decision = evaluate_intent(
        _intent(),
        _limits(),
        open_intent_count=0,
        kill_switch_active=True,
    )
    count_decision = evaluate_intent(_intent(), _limits(), open_intent_count=2)

    assert kill_decision.reason_code == "kill_switch_active"
    assert count_decision.reason_code == "open_intent_limit_exceeded"


def test_risk_limits_validate_configuration() -> None:
    """Invalid risk limit configuration is rejected."""
    with pytest.raises(ValueError):
        RiskLimits(max_stake_per_intent=Decimal("0"), max_open_intents=1)
    with pytest.raises(ValueError):
        RiskLimits(max_stake_per_intent=Decimal("1"), max_open_intents=-1)
