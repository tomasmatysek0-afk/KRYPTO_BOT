"""Tests for guard order intent domain models."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from coinbase_freqtrade_guarded_bot.guard_layer.order_intent import (
    GuardModelError,
    OrderIntent,
    RiskDecision,
)


def test_order_intent_serializes_audit_safe_values() -> None:
    """OrderIntent serializes Decimal and datetime values safely."""
    intent = OrderIntent(
        intent_id="intent-1",
        pair="BTC/USD",
        side="buy",
        position_effect="open",
        stake_amount=Decimal("100"),
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
    )

    audit_data = intent.to_audit_dict()

    assert audit_data["stake_amount"] == "100"
    assert audit_data["leverage"] == "1"
    assert audit_data["created_at"] == "2026-01-01T00:00:00+00:00"


def test_order_intent_rejects_invalid_inputs() -> None:
    """Invalid intent models fail before risk evaluation."""
    with pytest.raises(GuardModelError):
        OrderIntent("", "BTC/USD", "buy", "open", Decimal("100"))
    with pytest.raises(GuardModelError):
        OrderIntent("intent-1", "DOGE/USD", "buy", "open", Decimal("100"))
    with pytest.raises(GuardModelError):
        OrderIntent("intent-1", "BTC/USD", "buy", "open", Decimal("100"), quote_currency="USDC")
    with pytest.raises(GuardModelError):
        OrderIntent("intent-1", "BTC/USD", "buy", "open", Decimal("0"))
    with pytest.raises(GuardModelError):
        OrderIntent("intent-1", "BTC/USD", "buy", "open", Decimal("100"), leverage=Decimal("0"))
    with pytest.raises(GuardModelError):
        OrderIntent(
            "intent-1",
            "BTC/USD",
            "buy",
            "open",
            Decimal("100"),
            created_at=datetime(2026, 1, 1),
        )


def test_risk_decision_rejects_invalid_inputs() -> None:
    """RiskDecision requires auditable reason data."""
    intent = OrderIntent("intent-1", "BTC/USD", "buy", "open", Decimal("100"))
    approved = RiskDecision.approve(intent)

    assert approved.approved
    assert approved.to_audit_dict()["reason_code"] == "approved"

    with pytest.raises(GuardModelError):
        RiskDecision("", True, "approved", "ok")
    with pytest.raises(GuardModelError):
        RiskDecision("intent-1", True, "", "ok")
    with pytest.raises(GuardModelError):
        RiskDecision("intent-1", True, "approved", "ok", checked_at=datetime(2026, 1, 1))
