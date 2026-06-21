"""Conservative Freqtrade baseline strategy for Coinbase BTC/USD and ETH/USD."""

from __future__ import annotations

from freqtrade.strategy import IStrategy, informative
from pandas import DataFrame


class CoinbaseTrendGuardV1(IStrategy):
    """Long-only spot baseline strategy with trend, momentum, and risk guards."""

    INTERFACE_VERSION = 3

    timeframe = "4h"
    can_short = False
    startup_candle_count = 120
    process_only_new_candles = True

    minimal_roi = {
        "0": 0.04,
        "96": 0.02,
        "192": 0.0,
    }
    stoploss = -0.10
    trailing_stop = False
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    order_types = {
        "entry": "limit",
        "exit": "limit",
        "stoploss": "market",
        "stoploss_on_exchange": False,
    }
    order_time_in_force = {
        "entry": "GTC",
        "exit": "GTC",
    }

    @informative("1d")
    def populate_indicators_1d(
        self,
        dataframe: DataFrame,
        metadata: dict[str, object],
    ) -> DataFrame:
        """Add the daily trend filter used by 4h entry rules."""
        dataframe["ema_trend"] = dataframe["close"].ewm(span=50, adjust=False).mean()
        dataframe["trend_ok"] = dataframe["close"] > dataframe["ema_trend"]
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict[str, object]) -> DataFrame:
        """Add 4h baseline indicators without external TA dependencies."""
        dataframe["ema_fast"] = dataframe["close"].ewm(span=12, adjust=False).mean()
        dataframe["ema_slow"] = dataframe["close"].ewm(span=36, adjust=False).mean()
        dataframe["momentum_3"] = dataframe["close"].pct_change(3)
        dataframe["volume_mean"] = dataframe["volume"].rolling(20, min_periods=20).mean()
        candle_range = (dataframe["high"] - dataframe["low"]) / dataframe["close"]
        dataframe["range_ratio"] = candle_range.rolling(14, min_periods=14).mean()
        dataframe["extension_ratio"] = (dataframe["close"] / dataframe["ema_fast"]) - 1
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict[str, object]) -> DataFrame:
        """Mark conservative long entries only when all baseline filters agree."""
        trend_filter = dataframe.get("trend_ok_1d", dataframe["close"] != dataframe["close"])
        entry_condition = (
            (dataframe["volume"] > 0)
            & (dataframe["volume"] > dataframe["volume_mean"])
            & (dataframe["close"] > dataframe["ema_slow"])
            & (dataframe["ema_fast"] > dataframe["ema_slow"])
            & (dataframe["momentum_3"] > 0)
            & (dataframe["range_ratio"] < 0.08)
            & (dataframe["extension_ratio"] < 0.06)
            & trend_filter
        )

        dataframe.loc[entry_condition, ["enter_long", "enter_tag"]] = (1, "baseline_trend_guard")
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict[str, object]) -> DataFrame:
        """Mark exits when trend or momentum conditions deteriorate."""
        trend_filter = dataframe.get("trend_ok_1d", dataframe["close"] == dataframe["close"])
        exit_condition = (
            (dataframe["close"] < dataframe["ema_fast"])
            | (dataframe["momentum_3"] < 0)
            | (~trend_filter)
        )

        dataframe.loc[exit_condition, ["exit_long", "exit_tag"]] = (1, "baseline_guard_exit")
        return dataframe
