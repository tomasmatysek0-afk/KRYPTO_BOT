"""Import smoke tests for the package skeleton."""

from __future__ import annotations

import importlib

import coinbase_freqtrade_guarded_bot


def test_package_exposes_version() -> None:
    """The package exposes a stable version string."""
    assert coinbase_freqtrade_guarded_bot.__version__ == "0.1.0"


def test_phase_00b_subpackages_import() -> None:
    """The Phase 00b package layout is importable without cwd hacks."""
    modules = [
        "coinbase_freqtrade_guarded_bot.cli",
        "coinbase_freqtrade_guarded_bot.config",
        "coinbase_freqtrade_guarded_bot.data_layer",
        "coinbase_freqtrade_guarded_bot.guard_layer",
        "coinbase_freqtrade_guarded_bot.network",
        "coinbase_freqtrade_guarded_bot.reporting",
        "coinbase_freqtrade_guarded_bot.research",
        "coinbase_freqtrade_guarded_bot.storage",
        "coinbase_freqtrade_guarded_bot.tax_layer",
        "coinbase_freqtrade_guarded_bot.tax_layer.migrations",
        "coinbase_freqtrade_guarded_bot.ui_support",
        "coinbase_freqtrade_guarded_bot.utils",
    ]

    for module_name in modules:
        assert importlib.import_module(module_name)
