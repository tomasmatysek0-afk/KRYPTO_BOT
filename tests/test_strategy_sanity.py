"""Static sanity checks for the Freqtrade baseline strategy."""

from __future__ import annotations

import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STRATEGY_PATH = PROJECT_ROOT / "user_data" / "strategies" / "CoinbaseTrendGuardV1.py"
DRYRUN_CONFIG = PROJECT_ROOT / "user_data" / "config" / "config.dryrun.json"
FORBIDDEN_STRATEGY_TEXT = (
    "sys.path",
    "requests",
    "ccxt",
    "coinbase",
    "create_order",
    "cancel_order",
    "leverage",
    "margin",
    "futures",
    "can_short = True",
)


def _strategy_tree() -> ast.Module:
    """Parse the strategy source without importing Freqtrade locally."""
    return ast.parse(STRATEGY_PATH.read_text(encoding="utf-8"))


def _strategy_class() -> ast.ClassDef:
    """Return the baseline strategy class node."""
    for node in _strategy_tree().body:
        if isinstance(node, ast.ClassDef) and node.name == "CoinbaseTrendGuardV1":
            return node
    raise AssertionError("CoinbaseTrendGuardV1 class not found")


def _class_assignment_value(name: str) -> object:
    """Return a literal class assignment value from the strategy class."""
    for node in _strategy_class().body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise AssertionError(f"{name} assignment not found")


def test_strategy_file_exists_and_has_no_import_hacks_or_live_clients() -> None:
    """Strategy source contains no path hacks, API clients, or live order calls."""
    strategy_text = STRATEGY_PATH.read_text(encoding="utf-8")

    assert STRATEGY_PATH.exists()
    for forbidden_text in FORBIDDEN_STRATEGY_TEXT:
        assert forbidden_text not in strategy_text


def test_strategy_declares_long_only_spot_baseline_settings() -> None:
    """Static strategy settings stay inside MVP limits."""
    assert _class_assignment_value("timeframe") == "4h"
    assert _class_assignment_value("can_short") is False
    assert _class_assignment_value("process_only_new_candles") is True
    assert _class_assignment_value("startup_candle_count") >= 120
    assert _class_assignment_value("stoploss") < 0


def test_strategy_uses_daily_informative_trend_filter() -> None:
    """The strategy includes a 1d informative trend filter."""
    strategy_class = _strategy_class()
    informative_methods = [
        node
        for node in strategy_class.body
        if isinstance(node, ast.FunctionDef)
        and any(
            isinstance(decorator, ast.Call)
            and getattr(decorator.func, "id", None) == "informative"
            and decorator.args
            and isinstance(decorator.args[0], ast.Constant)
            and decorator.args[0].value == "1d"
            for decorator in node.decorator_list
        )
    ]

    assert [method.name for method in informative_methods] == ["populate_indicators_1d"]


def test_strategy_has_entry_exit_methods_and_tags() -> None:
    """The strategy exposes Freqtrade entry/exit hooks with audit-friendly tags."""
    strategy_text = STRATEGY_PATH.read_text(encoding="utf-8")
    method_names = {
        node.name for node in _strategy_class().body if isinstance(node, ast.FunctionDef)
    }

    assert "populate_indicators" in method_names
    assert "populate_entry_trend" in method_names
    assert "populate_exit_trend" in method_names
    assert "baseline_trend_guard" in strategy_text
    assert "baseline_guard_exit" in strategy_text


def test_dryrun_config_references_strategy_name() -> None:
    """The Docker/Freqtrade skeleton references the baseline strategy name."""
    config_text = DRYRUN_CONFIG.read_text(encoding="utf-8")
    compose_text = (PROJECT_ROOT / "docker-compose.yml").read_text(encoding="utf-8")

    assert "CoinbaseTrendGuardV1" in compose_text
    assert "dry_run" in config_text
