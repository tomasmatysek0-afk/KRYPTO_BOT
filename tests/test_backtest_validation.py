"""Deterministic tests for offline backtest validation metrics."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from coinbase_freqtrade_guarded_bot.research.backtest_validation import (
    BacktestValidationError,
    CostScenario,
    EquityPoint,
    PricePoint,
    TradeResult,
    WalkForwardWindow,
    build_sample_offline_report,
    build_walk_forward_report,
    calculate_buy_and_hold,
    calculate_equity_curve_metrics,
    calculate_exposure_ratio,
    calculate_trade_metrics,
    monte_carlo_trade_order_resampling,
    run_fee_slippage_sensitivity,
    write_json_report,
    write_markdown_report,
)


def _trade(
    trade_id: str,
    opened_day: int,
    closed_day: int,
    *,
    entry_price: str = "100",
    exit_price: str = "110",
    quantity: str = "1",
    entry_fee: str = "0",
    exit_fee: str = "0",
    slippage_cost: str = "0",
    enter_tag: str = "test_tag",
) -> TradeResult:
    return TradeResult(
        trade_id=trade_id,
        pair="BTC/USD",
        opened_at=datetime(2026, 1, opened_day, tzinfo=UTC),
        closed_at=datetime(2026, 1, closed_day, tzinfo=UTC),
        entry_price=Decimal(entry_price),
        exit_price=Decimal(exit_price),
        quantity=Decimal(quantity),
        entry_fee=Decimal(entry_fee),
        exit_fee=Decimal(exit_fee),
        slippage_cost=Decimal(slippage_cost),
        enter_tag=enter_tag,
    )


def test_trade_result_rejects_invalid_inputs() -> None:
    """Unsafe or out-of-scope trade inputs fail closed."""
    with pytest.raises(BacktestValidationError):
        TradeResult(
            trade_id="bad-pair",
            pair="DOGE/USD",
            opened_at=datetime(2026, 1, 1, tzinfo=UTC),
            closed_at=datetime(2026, 1, 2, tzinfo=UTC),
            entry_price=Decimal("100"),
            exit_price=Decimal("110"),
            quantity=Decimal("1"),
        )
    with pytest.raises(BacktestValidationError):
        _trade("bad-time", 2, 1)
    with pytest.raises(BacktestValidationError):
        _trade("bad-cost", 1, 2, entry_fee="-1")
    with pytest.raises(BacktestValidationError):
        TradeResult(
            trade_id="naive",
            pair="BTC/USD",
            opened_at=datetime(2026, 1, 1),
            closed_at=datetime(2026, 1, 2, tzinfo=UTC),
            entry_price=Decimal("100"),
            exit_price=Decimal("110"),
            quantity=Decimal("1"),
        )


def test_trade_metrics_cover_profit_factor_and_loss_streak() -> None:
    """Trade-list metrics include costs, win rate, profit factor, and loss streak."""
    trades = (
        _trade("win-1", 1, 2, exit_price="112", entry_fee="1", exit_fee="1"),
        _trade("loss-1", 3, 4, exit_price="95", slippage_cost="1"),
        _trade("loss-2", 5, 6, exit_price="96", slippage_cost="2"),
        _trade("win-2", 7, 8, exit_price="120", enter_tag="other_tag"),
    )

    metrics = calculate_trade_metrics(trades)

    assert metrics.trade_count == 4
    assert metrics.winning_trades == 2
    assert metrics.losing_trades == 2
    assert metrics.total_profit == Decimal("18")
    assert metrics.total_fees == Decimal("2")
    assert metrics.total_slippage == Decimal("3")
    assert metrics.win_rate == Decimal("0.5")
    assert metrics.average_profit_per_trade == Decimal("4.5")
    assert metrics.profit_factor == Decimal("30") / Decimal("12")
    assert metrics.max_loss_streak == 2
    assert metrics.best_trade_profit == Decimal("20")
    assert metrics.worst_trade_profit == Decimal("-6")
    assert [item.enter_tag for item in metrics.enter_tag_breakdown] == ["other_tag", "test_tag"]


def test_empty_trade_metrics_are_zero_with_undefined_profit_factor() -> None:
    """Empty local trade lists return zero metrics without fabricating profit factor."""
    metrics = calculate_trade_metrics(())

    assert metrics.trade_count == 0
    assert metrics.total_profit == Decimal("0")
    assert metrics.win_rate == Decimal("0")
    assert metrics.profit_factor is None
    assert metrics.enter_tag_breakdown == ()


def test_equity_curve_metrics_cover_drawdown_and_monthly_returns() -> None:
    """Equity-curve metrics include max drawdown and monthly return data."""
    points = (
        EquityPoint(datetime(2026, 1, 1, tzinfo=UTC), Decimal("1000")),
        EquityPoint(datetime(2026, 1, 2, tzinfo=UTC), Decimal("1100")),
        EquityPoint(datetime(2026, 1, 3, tzinfo=UTC), Decimal("990")),
        EquityPoint(datetime(2026, 2, 1, tzinfo=UTC), Decimal("1200")),
    )

    metrics = calculate_equity_curve_metrics(points)

    assert metrics.starting_equity == Decimal("1000")
    assert metrics.ending_equity == Decimal("1200")
    assert metrics.total_return == Decimal("0.2")
    assert metrics.max_drawdown == Decimal("0.1")
    assert [item.year_month for item in metrics.monthly_returns] == ["2026-01", "2026-02"]
    assert metrics.monthly_returns[0].return_rate == Decimal("-0.01")
    assert metrics.drawdown_curve[2].drawdown == Decimal("0.1")


def test_equity_and_price_series_reject_duplicate_timestamps() -> None:
    """Duplicate series timestamps fail rather than being silently merged."""
    timestamp = datetime(2026, 1, 1, tzinfo=UTC)

    with pytest.raises(BacktestValidationError):
        calculate_equity_curve_metrics(
            (
                EquityPoint(timestamp, Decimal("1000")),
                EquityPoint(timestamp, Decimal("1001")),
            )
        )
    with pytest.raises(BacktestValidationError):
        calculate_buy_and_hold(
            (
                PricePoint(timestamp, Decimal("100")),
                PricePoint(timestamp, Decimal("101")),
            ),
            initial_cash=Decimal("1000"),
        )


def test_exposure_ratio_counts_window_overlap_and_clamps() -> None:
    """Exposure uses only overlap inside the requested test window."""
    start = datetime(2026, 1, 1, tzinfo=UTC)
    end = datetime(2026, 1, 5, tzinfo=UTC)
    trades = (
        _trade("half-window", 1, 3),
        _trade("overlap", 2, 5),
    )

    exposure = calculate_exposure_ratio(trades, start=start, end=end)

    assert exposure == Decimal("1")
    with pytest.raises(BacktestValidationError):
        calculate_exposure_ratio(trades, start=end, end=start)


def test_fee_slippage_sensitivity_uses_numeric_scenario_table() -> None:
    """Cost sensitivity returns numeric scenario outputs from local trades."""
    trades = (
        _trade("win", 1, 2, exit_price="120"),
        _trade("loss", 3, 4, exit_price="95"),
    )
    scenarios = (
        CostScenario("base_fee", Decimal("0.001"), Decimal("0.0005")),
        CostScenario("slippage_high", Decimal("0.001"), Decimal("0.003")),
    )

    results = run_fee_slippage_sensitivity(
        trades,
        scenarios,
        initial_equity=Decimal("1000"),
    )

    assert len(results) == 2
    assert results[0].total_profit > results[1].total_profit
    assert results[0].total_return == results[0].total_profit / Decimal("1000")
    assert results[0].win_rate == Decimal("0.5")


def test_monte_carlo_resampling_is_deterministic_and_numeric() -> None:
    """Monte Carlo output contains deterministic numeric percentile fields."""
    trades = (
        _trade("win-1", 1, 2, exit_price="130"),
        _trade("loss-1", 3, 4, exit_price="80"),
        _trade("win-2", 5, 6, exit_price="115"),
        _trade("loss-2", 7, 8, exit_price="90"),
    )

    first = monte_carlo_trade_order_resampling(
        trades,
        initial_equity=Decimal("1000"),
        simulations=25,
        seed=42,
        drawdown_limit=Decimal("0.05"),
    )
    second = monte_carlo_trade_order_resampling(
        trades,
        initial_equity=Decimal("1000"),
        simulations=25,
        seed=42,
        drawdown_limit=Decimal("0.05"),
    )

    assert first == second
    assert first.number_of_simulations == 25
    assert first.percentile_cagr_5 == first.percentile_cagr_50 == first.percentile_cagr_95
    assert first.worst_simulated_drawdown > Decimal("0")
    assert Decimal("0") <= first.probability_drawdown_above_limit <= Decimal("1")
    assert Decimal("0") <= first.probability_negative_result_after_costs <= Decimal("1")


def test_walk_forward_report_contains_numeric_window_results() -> None:
    """Walk-forward output includes numeric fields from mock test windows."""
    initial_equity = Decimal("1000")
    first_trades = (_trade("wf-win", 1, 2, exit_price="120"),)
    second_trades = (_trade("wf-loss", 4, 5, exit_price="90"),)
    windows = (
        WalkForwardWindow(
            window_id="wf-1",
            train_start=datetime(2025, 12, 1, tzinfo=UTC),
            train_end=datetime(2025, 12, 15, tzinfo=UTC),
            test_start=datetime(2026, 1, 1, tzinfo=UTC),
            test_end=datetime(2026, 1, 3, tzinfo=UTC),
            trades=first_trades,
            equity_curve=(
                EquityPoint(datetime(2026, 1, 1, tzinfo=UTC), initial_equity),
                EquityPoint(datetime(2026, 1, 2, tzinfo=UTC), Decimal("1020")),
            ),
        ),
        WalkForwardWindow(
            window_id="wf-2",
            train_start=datetime(2025, 12, 16, tzinfo=UTC),
            train_end=datetime(2025, 12, 30, tzinfo=UTC),
            test_start=datetime(2026, 1, 4, tzinfo=UTC),
            test_end=datetime(2026, 1, 6, tzinfo=UTC),
            trades=second_trades,
            equity_curve=(
                EquityPoint(datetime(2026, 1, 4, tzinfo=UTC), initial_equity),
                EquityPoint(datetime(2026, 1, 5, tzinfo=UTC), Decimal("990")),
            ),
        ),
    )

    report = build_walk_forward_report(windows, max_drawdown_limit=Decimal("0.10"))

    assert report.number_of_windows == 2
    assert report.train_window_days == 14
    assert report.test_window_days == 2
    assert report.profitable_windows == 1
    assert report.losing_windows == 1
    assert report.aggregated_profit == Decimal("10")
    assert report.aggregated_max_drawdown == Decimal("0.01")


def test_buy_and_hold_comparison_uses_local_prices_and_costs() -> None:
    """Buy-and-hold comparison is calculated from local price points only."""
    prices = (
        PricePoint(datetime(2026, 1, 1, tzinfo=UTC), Decimal("100")),
        PricePoint(datetime(2026, 1, 11, tzinfo=UTC), Decimal("110")),
    )

    no_cost = calculate_buy_and_hold(prices, initial_cash=Decimal("1000"))
    with_costs = calculate_buy_and_hold(
        prices,
        initial_cash=Decimal("1000"),
        fee_rate=Decimal("0.001"),
        slippage_rate=Decimal("0.001"),
    )

    assert no_cost.quantity == Decimal("10")
    assert no_cost.ending_value == Decimal("1100")
    assert no_cost.total_profit == Decimal("100")
    assert with_costs.ending_value < no_cost.ending_value


def test_report_generation_contains_local_pass_and_docker_deferred(tmp_path: Path) -> None:
    """Markdown and JSON reports contain numeric local outputs and deferred runtime status."""
    report = build_sample_offline_report()
    markdown_path = tmp_path / "report.md"
    json_path = tmp_path / "report.json"

    write_markdown_report(report, markdown_path)
    write_json_report(report, json_path)

    markdown = markdown_path.read_text(encoding="utf-8")
    payload = report.to_json_dict()

    assert "LOCAL_OFFLINE_PASS" in markdown
    assert "DEFERRED_DOCKER_REQUIRED" in markdown
    assert "not evidence that real Freqtrade backtesting" in markdown
    assert "Simulations: 250" in markdown
    assert json_path.exists()
    assert isinstance(payload["monte_carlo"], dict)
    assert payload["monte_carlo"]["number_of_simulations"] == 250
    assert isinstance(payload["monte_carlo"]["percentile_cagr_50"], float)
    assert isinstance(payload["walk_forward"], dict)
    assert payload["walk_forward"]["number_of_windows"] == 3
    assert isinstance(payload["fee_slippage_sensitivity"], list)
    assert len(payload["fee_slippage_sensitivity"]) == 5


def test_mock_backtest_report_artifacts_exist() -> None:
    """Phase 06 includes checked-in deterministic local report artifacts."""
    repo_root = Path(__file__).resolve().parents[1]
    markdown_path = repo_root / "reports" / "backtests" / "2026-06-21_mock_backtest_report.md"
    json_path = repo_root / "reports" / "backtests" / "2026-06-21_mock_backtest_report.json"

    assert markdown_path.exists()
    assert json_path.exists()
    markdown = markdown_path.read_text(encoding="utf-8")
    json_payload = json_path.read_text(encoding="utf-8")
    assert "LOCAL_OFFLINE_PASS" in markdown
    assert "DEFERRED_DOCKER_REQUIRED" in markdown
    assert '"number_of_simulations": 250' in json_payload
