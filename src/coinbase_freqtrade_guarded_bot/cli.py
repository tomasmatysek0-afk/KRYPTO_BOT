"""Command-line interface for safe research and dry-run workflows."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from coinbase_freqtrade_guarded_bot import __version__

PROGRAM_NAME = "coinbase_freqtrade_guarded_bot"


def build_parser() -> argparse.ArgumentParser:
    """Build the root command parser without registering live execution commands."""
    parser = argparse.ArgumentParser(
        prog=PROGRAM_NAME,
        description="Research, backtest, dry-run, and reporting helpers. No live trading commands.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", metavar="command")
    _add_placeholder_command(
        subparsers,
        "data-parity",
        "Prepare the data parity workflow placeholder; implemented in Phase 03b.",
    )
    _add_placeholder_command(
        subparsers,
        "backtest-report",
        "Prepare the backtest report workflow placeholder; implemented in Phase 07.",
    )
    _add_placeholder_command(
        subparsers,
        "dryrun-healthcheck",
        "Prepare the dry-run healthcheck workflow placeholder; implemented in Phase 08.",
    )
    _add_placeholder_command(
        subparsers,
        "tax-export",
        "Prepare the tax export workflow placeholder; implemented in Phase 12.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 0
    return int(handler(args))


def data_parity() -> int:
    """Console entry point for the future data parity command."""
    return main(["data-parity"])


def backtest_report() -> int:
    """Console entry point for the future backtest report command."""
    return main(["backtest-report"])


def dryrun_healthcheck() -> int:
    """Console entry point for the future dry-run healthcheck command."""
    return main(["dryrun-healthcheck"])


def tax_export() -> int:
    """Console entry point for the future tax export command."""
    return main(["tax-export"])


def _add_placeholder_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    help_text: str,
) -> None:
    subparser = subparsers.add_parser(name, help=help_text, description=help_text)
    subparser.set_defaults(handler=_placeholder_command)


def _placeholder_command(args: argparse.Namespace) -> int:
    command = str(args.command)
    sys.stdout.write(
        f"{command} is registered as a safe placeholder and has no live execution path.\n"
    )
    return 0
