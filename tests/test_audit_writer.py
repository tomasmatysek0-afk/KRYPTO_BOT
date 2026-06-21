"""Tests for append-only guard audit writing."""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pytest

from coinbase_freqtrade_guarded_bot.guard_layer.audit_writer import AuditWriteError, AuditWriter
from coinbase_freqtrade_guarded_bot.guard_layer.order_intent import OrderIntent
from coinbase_freqtrade_guarded_bot.guard_layer.risk_limits import (
    RiskLimits,
    evaluate_and_audit_intent,
)


def _intent(stake_amount: Decimal = Decimal("100")) -> OrderIntent:
    return OrderIntent(
        intent_id=f"intent-{stake_amount}",
        pair="BTC/USD",
        side="buy",
        position_effect="open",
        stake_amount=stake_amount,
    )


def test_audit_writer_appends_jsonl_decisions(tmp_path: Path) -> None:
    """AuditWriter appends one JSON object per line."""
    audit_path = tmp_path / "audit" / "guard.jsonl"
    writer = AuditWriter(audit_path)
    limits = RiskLimits(max_stake_per_intent=Decimal("250"), max_open_intents=2)

    first = evaluate_and_audit_intent(
        _intent(Decimal("100")),
        limits,
        writer,
        open_intent_count=0,
        kill_switch_path=tmp_path / "missing",
    )
    second = evaluate_and_audit_intent(
        _intent(Decimal("300")),
        limits,
        writer,
        open_intent_count=0,
        kill_switch_path=tmp_path / "missing",
    )

    records = [json.loads(line) for line in audit_path.read_text(encoding="utf-8").splitlines()]

    assert first.approved
    assert not second.approved
    assert len(records) == 2
    assert records[0]["decision"]["approved"] is True
    assert records[1]["decision"]["reason_code"] == "stake_limit_exceeded"


def test_audit_writer_raises_domain_error_when_path_is_unwritable(tmp_path: Path) -> None:
    """Audit write failures surface as AuditWriteError."""
    blocked_parent = tmp_path / "blocked"
    blocked_parent.write_text("not a directory", encoding="utf-8")
    writer = AuditWriter(blocked_parent / "guard.jsonl")
    limits = RiskLimits(max_stake_per_intent=Decimal("250"), max_open_intents=2)
    decision = evaluate_and_audit_intent

    with pytest.raises(AuditWriteError):
        decision(
            _intent(),
            limits,
            writer,
            open_intent_count=0,
            kill_switch_path=tmp_path / "missing",
        )
