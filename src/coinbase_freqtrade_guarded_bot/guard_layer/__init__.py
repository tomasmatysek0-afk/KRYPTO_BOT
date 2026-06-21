"""Risk, audit, kill-switch, reconciliation, and data parity helpers."""

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

__all__ = [
    "Candle",
    "DataParityError",
    "ParityConfig",
    "ParityIssue",
    "ParityResult",
    "aggregate_1h_to_4h",
    "coinbase_product_id",
    "compare_candles",
    "is_closed_candle",
    "render_markdown_report",
    "write_markdown_report",
]
