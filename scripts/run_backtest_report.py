"""Generate deterministic offline backtest reports without Docker or network access."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from coinbase_freqtrade_guarded_bot.research.backtest_validation import (
    build_sample_offline_report,
    write_json_report,
    write_markdown_report,
)

DEFAULT_MARKDOWN_OUTPUT = Path("reports/backtests/2026-06-21_mock_backtest_report.md")
DEFAULT_JSON_OUTPUT = Path("reports/backtests/2026-06-21_mock_backtest_report.json")


def build_parser() -> argparse.ArgumentParser:
    """Build the offline report parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Generate a deterministic offline mock backtest report. "
            "No Docker, network, credentials, or live trading."
        ),
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=DEFAULT_MARKDOWN_OUTPUT,
        help="Markdown report path.",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=DEFAULT_JSON_OUTPUT,
        help="JSON report path.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Generate deterministic Phase 06 offline reports and return an exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)
    report = build_sample_offline_report()
    write_markdown_report(report, args.markdown_output)
    write_json_report(report, args.json_output)
    print(f"Wrote offline markdown report to {args.markdown_output}")
    print(f"Wrote offline JSON report to {args.json_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

