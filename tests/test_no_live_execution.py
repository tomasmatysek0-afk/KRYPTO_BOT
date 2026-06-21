"""Static safety tests for Freqtrade skeleton configuration."""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = PROJECT_ROOT / "user_data" / "config"
CONFIG_FILES = (
    CONFIG_DIR / "config.dryrun.json",
    CONFIG_DIR / "config.backtest.json",
)
PAIRLIST_FILE = CONFIG_DIR / "pairlist.json"
COMPOSE_FILE = PROJECT_ROOT / "docker-compose.yml"
STRATEGY_DIR = PROJECT_ROOT / "user_data" / "strategies"
ALLOWED_PAIRS = {"BTC/USD", "ETH/USD"}
ALLOWED_QUOTE = "USD"
FORBIDDEN_PAIR_SUBSTRINGS = ("USDT", "USDC", "EUR", "GBP", "DOGE", "SOL", "XRP")
SECRET_FIELD_NAMES = {"key", "secret", "password", "token", "uid", "ws_token"}


def _load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from a repository-relative path."""
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _walk_json(value: Any) -> Iterator[tuple[str, Any]]:
    """Yield flattened JSON key/value pairs for static policy checks."""
    if isinstance(value, dict):
        for key, nested_value in value.items():
            yield key, nested_value
            yield from _walk_json(nested_value)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_json(item)


def test_freqtrade_configs_are_safe_spot_dry_run_only() -> None:
    """Freqtrade configs cannot enable live, margin, futures, shorts, or altcoins."""
    for config_path in CONFIG_FILES:
        config = _load_json(config_path)
        exchange = config["exchange"]
        pair_whitelist = set(exchange["pair_whitelist"])

        assert config["dry_run"] is True
        assert config["trading_mode"] == "spot"
        assert config["margin_mode"] == ""
        assert config["stake_currency"] == ALLOWED_QUOTE
        assert config["fiat_display_currency"] == ALLOWED_QUOTE
        assert config["force_entry_enable"] is False
        assert config["api_server"]["enabled"] is False
        assert config["telegram"]["enabled"] is False
        assert pair_whitelist == ALLOWED_PAIRS
        assert exchange["pair_blacklist"] == []
        assert config["pairlists"] == [{"method": "StaticPairList"}]
        assert all(pair.endswith(f"/{ALLOWED_QUOTE}") for pair in pair_whitelist)
        assert not any(
            forbidden in pair
            for pair in pair_whitelist
            for forbidden in FORBIDDEN_PAIR_SUBSTRINGS
        )


def test_freqtrade_configs_contain_no_secret_fields() -> None:
    """Static configs must not contain API credentials or secret placeholders."""
    for config_path in CONFIG_FILES:
        config = _load_json(config_path)
        flattened_keys = {key.lower() for key, _ in _walk_json(config)}

        assert flattened_keys.isdisjoint(SECRET_FIELD_NAMES)


def test_pairlist_matches_configured_coinbase_spot_pairs() -> None:
    """The standalone pairlist mirrors the Freqtrade config pair whitelist."""
    pairlist = _load_json(PAIRLIST_FILE)

    assert set(pairlist["pair_whitelist"]) == ALLOWED_PAIRS
    assert pairlist["pair_blacklist"] == []
    assert pairlist["pairlists"] == [{"method": "StaticPairList"}]

    for config_path in CONFIG_FILES:
        config = _load_json(config_path)
        assert config["exchange"]["pair_whitelist"] == pairlist["pair_whitelist"]
        assert config["exchange"]["pair_blacklist"] == pairlist["pair_blacklist"]
        assert config["pairlists"] == pairlist["pairlists"]


def test_docker_compose_is_portable_and_not_publicly_exposed() -> None:
    """Compose skeleton uses relative mounts and exposes no public API port."""
    compose_text = COMPOSE_FILE.read_text(encoding="utf-8")

    assert "- ./user_data:/freqtrade/user_data" in compose_text
    assert "- ./src:/freqtrade/src:ro" in compose_text
    assert "PYTHONPATH: /freqtrade/src" in compose_text
    assert "/freqtrade/user_data/config/config.dryrun.json" in compose_text
    assert "ports:" not in compose_text
    assert "0.0.0.0" not in compose_text
    assert "ALLOW_LIVE_TRADING" not in compose_text
    assert "config-private" not in compose_text


def test_strategy_files_do_not_modify_python_path() -> None:
    """Freqtrade strategy files must not use cwd or sys.path import hacks."""
    assert STRATEGY_DIR.is_dir()

    for strategy_path in STRATEGY_DIR.glob("*.py"):
        strategy_text = strategy_path.read_text(encoding="utf-8")
        assert "sys.path" not in strategy_text
        assert "site.addsitedir" not in strategy_text
