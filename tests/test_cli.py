"""CLI smoke tests."""

from __future__ import annotations

import subprocess
import sys

from coinbase_freqtrade_guarded_bot.cli import build_parser, main


def test_cli_help_lists_safe_placeholders() -> None:
    """CLI help is available and contains no order-execution command."""
    result = subprocess.run(
        [sys.executable, "-m", "coinbase_freqtrade_guarded_bot", "--help"],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0
    assert "data-parity" in result.stdout
    assert "backtest-report" in result.stdout
    assert "dryrun-healthcheck" in result.stdout
    assert "tax-export" in result.stdout
    assert "create-order" not in result.stdout
    assert "cancel-order" not in result.stdout


def test_cli_placeholder_returns_success(capsys) -> None:
    """Placeholder commands are safe no-op entry points."""
    exit_code = main(["data-parity"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "no live execution path" in captured.out


def test_parser_has_no_live_subcommand() -> None:
    """The parser does not register live trading commands."""
    parser = build_parser()
    help_text = parser.format_help()

    assert "live" not in {action.dest for action in parser._actions}
    assert "create-order" not in help_text
    assert "cancel-order" not in help_text
