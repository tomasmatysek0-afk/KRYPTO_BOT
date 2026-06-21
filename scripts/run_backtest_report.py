"""Generate deterministic offline backtest reports without Docker or network access."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from coinbase_freqtrade_guarded_bot.research.backtest_validation import (
    build_sample_offline_report,
    write_json_report,
    write_markdown_report,
    write_report_bundle,
)

DEFAULT_OUTPUT_DIR = Path("reports/backtests")
DEFAULT_REPORT_DATE = "2026-06-21"


def build_parser() -> argparse.ArgumentParser:
    """Build the offline report parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Generate a deterministic offline mock backtest report. "
            "No Docker, network, credentials, or live trading."
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for generated report artifacts.",
    )
    parser.add_argument(
        "--report-date",
        default=DEFAULT_REPORT_DATE,
        help="Filename date prefix for report artifacts.",
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=None,
        help="Optional legacy combined markdown report path.",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=None,
        help="Optional legacy combined JSON report path.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Generate deterministic Phase 07 offline reports and return an exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)
    report = build_sample_offline_report()
    bundle_paths = write_report_bundle(
        report,
        args.output_dir,
        report_date=args.report_date,
    )
    markdown_output = args.markdown_output or (
        args.output_dir / f"{args.report_date}_mock_backtest_report.md"
    )
    json_output = args.json_output or (
        args.output_dir / f"{args.report_date}_mock_backtest_report.json"
    )
    write_markdown_report(report, markdown_output)
    write_json_report(report, json_output)
    print(f"Wrote strategy summary to {bundle_paths.strategy_summary}")
    print(f"Wrote trades CSV to {bundle_paths.trades_csv}")
    print(f"Wrote metrics JSON to {bundle_paths.metrics_json}")
    print(f"Wrote drawdown CSV to {bundle_paths.drawdown_csv}")
    print(f"Wrote walk-forward JSON to {bundle_paths.walkforward_json}")
    print(f"Wrote Monte Carlo JSON to {bundle_paths.montecarlo_json}")
    print(f"Wrote combined markdown report to {markdown_output}")
    print(f"Wrote combined JSON report to {json_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
