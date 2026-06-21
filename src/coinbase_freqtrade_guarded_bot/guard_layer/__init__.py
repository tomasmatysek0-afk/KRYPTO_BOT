"""Risk, audit, kill-switch, reconciliation, and data parity helpers."""

from coinbase_freqtrade_guarded_bot.guard_layer.audit_writer import AuditWriteError, AuditWriter
from coinbase_freqtrade_guarded_bot.guard_layer.data_parity import (
    Candle,
    DataParityError,
    ParityConfig,
    ParityIssue,
    ParityResult,
    aggregate_1h_to_4h,
    coinbase_product_id,
    compare_candles,
    is_closed_candle,
    render_markdown_report,
    write_markdown_report,
)
from coinbase_freqtrade_guarded_bot.guard_layer.kill_switch import is_kill_switch_active
from coinbase_freqtrade_guarded_bot.guard_layer.order_intent import (
    GuardModelError,
    OrderIntent,
    RiskDecision,
)
from coinbase_freqtrade_guarded_bot.guard_layer.risk_limits import (
    RiskLimits,
    evaluate_and_audit_intent,
    evaluate_intent,
)

__all__ = [
    "AuditWriteError",
    "AuditWriter",
    "Candle",
    "DataParityError",
    "GuardModelError",
    "OrderIntent",
    "ParityConfig",
    "ParityIssue",
    "ParityResult",
    "RiskDecision",
    "RiskLimits",
    "aggregate_1h_to_4h",
    "coinbase_product_id",
    "evaluate_and_audit_intent",
    "evaluate_intent",
    "is_kill_switch_active",
    "compare_candles",
    "is_closed_candle",
    "render_markdown_report",
    "write_markdown_report",
]
