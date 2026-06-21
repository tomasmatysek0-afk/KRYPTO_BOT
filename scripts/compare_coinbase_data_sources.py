"""Generate a mock data parity report without network or Docker access."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from coinbase_freqtrade_guarded_bot.guard_layer.data_parity import (
    Candle,
    ParityConfig,
    compare_candles,
    write_markdown_report,
)

DEFAULT_OUTPUT = Path("reports/data_parity/2026-06-21_mock_parity_report.md")


def build_parser() -> argparse.ArgumentParser:
    """Build the mock parity report parser."""
    parser = argparse.ArgumentParser(
        description="Generate an offline mock data parity report. No network or live trading.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Markdown report path.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Generate a deterministic mock parity report and return an exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)
    as_of = datetime(2026, 1, 1, 2, tzinfo=UTC)
    candle = Candle(
        pair="BTC/USD",
        timeframe="1h",
        timestamp=datetime(2026, 1, 1, 0, tzinfo=UTC),
        open=Decimal("100"),
        high=Decimal("110"),
        low=Decimal("90"),
        close=Decimal("105"),
        volume=Decimal("12.5"),
    )
    result = compare_candles(
        [candle],
        [candle],
        as_of=as_of,
        config=ParityConfig(),
        reference_source="mock_coinbase_advanced",
        candidate_source="mock_freqtrade_ccxt",
    )
    write_markdown_report(result, args.output)
    print(f"Wrote mock data parity report to {args.output}")
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
