"""Offline backtest validation metrics for deterministic local reports."""

from __future__ import annotations

import csv
import json
import random
from dataclasses import dataclass, fields, is_dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any, Literal, TypeAlias

Conclusion: TypeAlias = Literal["PASS", "FAIL", "RESEARCH_ONLY"]
SamplingMode: TypeAlias = Literal["shuffle"]

SUPPORTED_PAIRS = {"BTC/USD", "ETH/USD"}
DAYS_PER_YEAR = Decimal("365")
SECONDS_PER_YEAR = Decimal("31536000")
ZERO = Decimal("0")
ONE = Decimal("1")
REPORT_DISCLAIMER = (
    "Research-only offline sample report. This is not financial advice, not a profit "
    "guarantee, and not evidence that real Freqtrade backtesting or dry-run runtime "
    "validation has passed."
)
DEFERRED_DOCKER_ITEMS = (
    "real Freqtrade backtest execution",
    "real strategy runtime loading inside Freqtrade",
    "Docker-based Freqtrade backtest",
    "Docker-based data download",
    "real Coinbase/Freqtrade data parity",
    "dry-run runtime validation",
)


class BacktestValidationError(ValueError):
    """Raised when offline backtest validation inputs are invalid."""


@dataclass(frozen=True, slots=True)
class TradeResult:
    """Closed spot trade result used by offline metric calculations."""

    trade_id: str
    pair: str
    opened_at: datetime
    closed_at: datetime
    entry_price: Decimal
    exit_price: Decimal
    quantity: Decimal
    entry_fee: Decimal = ZERO
    exit_fee: Decimal = ZERO
    slippage_cost: Decimal = ZERO
    enter_tag: str = "baseline"

    def __post_init__(self) -> None:
        if not self.trade_id:
            raise BacktestValidationError("trade_id is required.")
        if self.pair not in SUPPORTED_PAIRS:
            raise BacktestValidationError(f"Unsupported pair: {self.pair}")
        if self.entry_price <= ZERO or self.exit_price <= ZERO:
            raise BacktestValidationError("entry_price and exit_price must be positive.")
        if self.quantity <= ZERO:
            raise BacktestValidationError("quantity must be positive.")
        if self.entry_fee < ZERO or self.exit_fee < ZERO or self.slippage_cost < ZERO:
            raise BacktestValidationError("cost fields must not be negative.")
        opened_at = _as_utc(self.opened_at)
        closed_at = _as_utc(self.closed_at)
        if closed_at <= opened_at:
            raise BacktestValidationError("closed_at must be after opened_at.")
        object.__setattr__(self, "opened_at", opened_at)
        object.__setattr__(self, "closed_at", closed_at)

    @property
    def entry_notional(self) -> Decimal:
        """Return entry notional in quote currency."""
        return self.entry_price * self.quantity

    @property
    def exit_notional(self) -> Decimal:
        """Return exit notional in quote currency."""
        return self.exit_price * self.quantity

    @property
    def gross_profit(self) -> Decimal:
        """Return gross profit before fees and slippage."""
        return self.exit_notional - self.entry_notional

    @property
    def total_costs(self) -> Decimal:
        """Return total explicit trading costs."""
        return self.entry_fee + self.exit_fee + self.slippage_cost

    @property
    def net_profit(self) -> Decimal:
        """Return net profit after fees and slippage."""
        return self.gross_profit - self.total_costs

    @property
    def return_rate(self) -> Decimal:
        """Return net trade return relative to entry notional."""
        return self.net_profit / self.entry_notional

    @property
    def duration(self) -> timedelta:
        """Return the closed trade duration."""
        return self.closed_at - self.opened_at


@dataclass(frozen=True, slots=True)
class EquityPoint:
    """Timestamped account equity point for offline curve metrics."""

    timestamp: datetime
    equity: Decimal

    def __post_init__(self) -> None:
        if self.equity <= ZERO:
            raise BacktestValidationError("equity must be positive.")
        object.__setattr__(self, "timestamp", _as_utc(self.timestamp))


@dataclass(frozen=True, slots=True)
class PricePoint:
    """Timestamped close price for local buy-and-hold comparison."""

    timestamp: datetime
    close: Decimal

    def __post_init__(self) -> None:
        if self.close <= ZERO:
            raise BacktestValidationError("close must be positive.")
        object.__setattr__(self, "timestamp", _as_utc(self.timestamp))


@dataclass(frozen=True, slots=True)
class DrawdownPoint:
    """Single drawdown point as a positive fraction from prior equity peak."""

    timestamp: datetime
    drawdown: Decimal


@dataclass(frozen=True, slots=True)
class MonthlyReturn:
    """Calendar-month return from the local equity curve."""

    year_month: str
    return_rate: Decimal


@dataclass(frozen=True, slots=True)
class EnterTagMetric:
    """Aggregated metrics for one strategy enter_tag."""

    enter_tag: str
    trade_count: int
    total_profit: Decimal


@dataclass(frozen=True, slots=True)
class TradeMetrics:
    """Aggregate trade-list metrics."""

    trade_count: int
    winning_trades: int
    losing_trades: int
    total_profit: Decimal
    total_fees: Decimal
    total_slippage: Decimal
    win_rate: Decimal
    average_profit_per_trade: Decimal
    profit_factor: Decimal | None
    max_loss_streak: int
    best_trade_profit: Decimal
    worst_trade_profit: Decimal
    enter_tag_breakdown: tuple[EnterTagMetric, ...]


@dataclass(frozen=True, slots=True)
class EquityCurveMetrics:
    """Aggregate equity-curve metrics."""

    starting_equity: Decimal
    ending_equity: Decimal
    total_return: Decimal
    cagr: Decimal
    max_drawdown: Decimal
    sharpe: Decimal
    sortino: Decimal
    monthly_returns: tuple[MonthlyReturn, ...]
    drawdown_curve: tuple[DrawdownPoint, ...]


@dataclass(frozen=True, slots=True)
class CostScenario:
    """Fee and slippage cost scenario for deterministic sensitivity checks."""

    name: str
    fee_rate: Decimal
    slippage_rate: Decimal

    def __post_init__(self) -> None:
        if not self.name:
            raise BacktestValidationError("scenario name is required.")
        if self.fee_rate < ZERO or self.slippage_rate < ZERO:
            raise BacktestValidationError("fee_rate and slippage_rate must not be negative.")


@dataclass(frozen=True, slots=True)
class CostScenarioResult:
    """Numeric result for one fee/slippage scenario."""

    name: str
    fee_rate: Decimal
    slippage_rate: Decimal
    total_profit: Decimal
    total_return: Decimal
    average_profit_per_trade: Decimal
    win_rate: Decimal
    profit_factor: Decimal | None


@dataclass(frozen=True, slots=True)
class MonteCarloSummary:
    """Summary of deterministic trade-order Monte Carlo resampling."""

    number_of_simulations: int
    seed: int
    sampling_mode: SamplingMode
    percentile_cagr_5: Decimal
    percentile_cagr_50: Decimal
    percentile_cagr_95: Decimal
    percentile_max_drawdown_5: Decimal
    percentile_max_drawdown_50: Decimal
    percentile_max_drawdown_95: Decimal
    worst_simulated_drawdown: Decimal
    probability_drawdown_above_limit: Decimal
    probability_negative_result_after_costs: Decimal


@dataclass(frozen=True, slots=True)
class WalkForwardWindow:
    """Local mock walk-forward input window."""

    window_id: str
    train_start: datetime
    train_end: datetime
    test_start: datetime
    test_end: datetime
    trades: tuple[TradeResult, ...]
    equity_curve: tuple[EquityPoint, ...]

    def __post_init__(self) -> None:
        if not self.window_id:
            raise BacktestValidationError("window_id is required.")
        train_start = _as_utc(self.train_start)
        train_end = _as_utc(self.train_end)
        test_start = _as_utc(self.test_start)
        test_end = _as_utc(self.test_end)
        if not (train_start < train_end <= test_start < test_end):
            raise BacktestValidationError("walk-forward train/test dates are invalid.")
        object.__setattr__(self, "train_start", train_start)
        object.__setattr__(self, "train_end", train_end)
        object.__setattr__(self, "test_start", test_start)
        object.__setattr__(self, "test_end", test_end)


@dataclass(frozen=True, slots=True)
class WalkForwardWindowResult:
    """Numeric result for one local mock walk-forward test window."""

    window_id: str
    train_window_days: int
    test_window_days: int
    trade_count: int
    total_profit: Decimal
    total_return: Decimal
    max_drawdown: Decimal
    profitable: bool


@dataclass(frozen=True, slots=True)
class WalkForwardReport:
    """Aggregated local mock walk-forward report."""

    number_of_windows: int
    train_window_days: int
    test_window_days: int
    window_results: tuple[WalkForwardWindowResult, ...]
    profitable_windows: int
    losing_windows: int
    aggregated_profit: Decimal
    aggregated_max_drawdown: Decimal
    conclusion: Conclusion


@dataclass(frozen=True, slots=True)
class BuyAndHoldResult:
    """Local buy-and-hold comparison result."""

    starting_price: Decimal
    ending_price: Decimal
    quantity: Decimal
    ending_value: Decimal
    total_profit: Decimal
    total_return: Decimal
    cagr: Decimal


@dataclass(frozen=True, slots=True)
class OfflineBacktestReport:
    """Complete local/offline Phase 06 report payload."""

    strategy_name: str
    config_version: str
    data_source_decision: str
    pairs: tuple[str, ...]
    timeframe: str
    generated_at: datetime
    fee_model: str
    slippage_model: str
    exposure: Decimal
    trades: tuple[TradeResult, ...]
    equity_curve: tuple[EquityPoint, ...]
    trade_metrics: TradeMetrics
    equity_metrics: EquityCurveMetrics
    buy_and_hold: BuyAndHoldResult
    fee_slippage_sensitivity: tuple[CostScenarioResult, ...]
    monte_carlo: MonteCarloSummary
    walk_forward: WalkForwardReport
    conclusion: Conclusion
    local_acceptance_status: str
    deferred_status: str
    deferred_items: tuple[str, ...]
    disclaimer: str = REPORT_DISCLAIMER

    def to_json_dict(self) -> dict[str, object]:
        """Return a JSON-compatible dictionary with numeric metric fields."""
        return _to_jsonable(self)

    def to_markdown(self) -> str:
        """Render this report as markdown."""
        return render_markdown_report(self)


@dataclass(frozen=True, slots=True)
class ReportBundlePaths:
    """Filesystem paths written by the Phase 07 local report bundle."""

    strategy_summary: Path
    trades_csv: Path
    metrics_json: Path
    drawdown_csv: Path
    walkforward_json: Path
    montecarlo_json: Path


def calculate_trade_metrics(trades: tuple[TradeResult, ...] | list[TradeResult]) -> TradeMetrics:
    """Calculate deterministic aggregate metrics from a closed trade list."""
    ordered_trades = tuple(sorted(trades, key=lambda trade: trade.closed_at))
    profits = [trade.net_profit for trade in ordered_trades]
    winning = [profit for profit in profits if profit > ZERO]
    losing = [profit for profit in profits if profit < ZERO]
    total_profit = sum(profits, ZERO)
    trade_count = len(ordered_trades)
    total_fees = sum((trade.entry_fee + trade.exit_fee for trade in ordered_trades), ZERO)
    total_slippage = sum((trade.slippage_cost for trade in ordered_trades), ZERO)
    gross_profit = sum(winning, ZERO)
    gross_loss = abs(sum(losing, ZERO))
    profit_factor = None if gross_loss == ZERO else gross_profit / gross_loss
    enter_tag_breakdown = _build_enter_tag_breakdown(ordered_trades)

    return TradeMetrics(
        trade_count=trade_count,
        winning_trades=len(winning),
        losing_trades=len(losing),
        total_profit=total_profit,
        total_fees=total_fees,
        total_slippage=total_slippage,
        win_rate=_safe_ratio(Decimal(len(winning)), Decimal(trade_count)),
        average_profit_per_trade=_safe_ratio(total_profit, Decimal(trade_count)),
        profit_factor=profit_factor,
        max_loss_streak=_calculate_max_loss_streak(profits),
        best_trade_profit=max(profits, default=ZERO),
        worst_trade_profit=min(profits, default=ZERO),
        enter_tag_breakdown=enter_tag_breakdown,
    )


def calculate_drawdown_curve(
    equity_curve: tuple[EquityPoint, ...] | list[EquityPoint],
) -> tuple[DrawdownPoint, ...]:
    """Calculate drawdown at each equity point as a positive fraction."""
    points = _ordered_equity_points(equity_curve)
    if not points:
        return ()
    peak = points[0].equity
    drawdowns: list[DrawdownPoint] = []
    for point in points:
        if point.equity > peak:
            peak = point.equity
        drawdown = ZERO if peak == ZERO else (peak - point.equity) / peak
        drawdowns.append(DrawdownPoint(timestamp=point.timestamp, drawdown=drawdown))
    return tuple(drawdowns)


def calculate_equity_curve_metrics(
    equity_curve: tuple[EquityPoint, ...] | list[EquityPoint],
) -> EquityCurveMetrics:
    """Calculate CAGR, drawdown, Sharpe, Sortino, and monthly returns."""
    points = _ordered_equity_points(equity_curve)
    if not points:
        raise BacktestValidationError("equity_curve must contain at least one point.")
    starting_equity = points[0].equity
    ending_equity = points[-1].equity
    total_return = ending_equity / starting_equity - ONE
    drawdown_curve = calculate_drawdown_curve(points)
    returns = _period_returns(points)

    return EquityCurveMetrics(
        starting_equity=starting_equity,
        ending_equity=ending_equity,
        total_return=total_return,
        cagr=_calculate_cagr(
            starting_equity,
            ending_equity,
            points[0].timestamp,
            points[-1].timestamp,
        ),
        max_drawdown=max((point.drawdown for point in drawdown_curve), default=ZERO),
        sharpe=_calculate_sharpe(returns, points),
        sortino=_calculate_sortino(returns, points),
        monthly_returns=_calculate_monthly_returns(points),
        drawdown_curve=drawdown_curve,
    )


def calculate_exposure_ratio(
    trades: tuple[TradeResult, ...] | list[TradeResult],
    *,
    start: datetime,
    end: datetime,
) -> Decimal:
    """Calculate time-in-market exposure as a fraction of a test window."""
    start_utc = _as_utc(start)
    end_utc = _as_utc(end)
    if end_utc <= start_utc:
        raise BacktestValidationError("exposure end must be after start.")
    total_seconds = Decimal(str((end_utc - start_utc).total_seconds()))
    exposed_seconds = ZERO
    for trade in trades:
        overlap_start = max(trade.opened_at, start_utc)
        overlap_end = min(trade.closed_at, end_utc)
        if overlap_end > overlap_start:
            exposed_seconds += Decimal(str((overlap_end - overlap_start).total_seconds()))
    return min(ONE, exposed_seconds / total_seconds)


def run_fee_slippage_sensitivity(
    trades: tuple[TradeResult, ...] | list[TradeResult],
    scenarios: tuple[CostScenario, ...] | list[CostScenario],
    *,
    initial_equity: Decimal,
) -> tuple[CostScenarioResult, ...]:
    """Reprice trades under deterministic fee/slippage scenarios."""
    if initial_equity <= ZERO:
        raise BacktestValidationError("initial_equity must be positive.")
    if not scenarios:
        raise BacktestValidationError("at least one cost scenario is required.")
    results: list[CostScenarioResult] = []
    for scenario in scenarios:
        adjusted_trades = tuple(_apply_cost_scenario(trade, scenario) for trade in trades)
        metrics = calculate_trade_metrics(adjusted_trades)
        results.append(
            CostScenarioResult(
                name=scenario.name,
                fee_rate=scenario.fee_rate,
                slippage_rate=scenario.slippage_rate,
                total_profit=metrics.total_profit,
                total_return=metrics.total_profit / initial_equity,
                average_profit_per_trade=metrics.average_profit_per_trade,
                win_rate=metrics.win_rate,
                profit_factor=metrics.profit_factor,
            )
        )
    return tuple(results)


def monte_carlo_trade_order_resampling(
    trades: tuple[TradeResult, ...] | list[TradeResult],
    *,
    initial_equity: Decimal,
    simulations: int,
    seed: int,
    drawdown_limit: Decimal,
) -> MonteCarloSummary:
    """Run deterministic Monte Carlo trade-order shuffling over local trade results."""
    if initial_equity <= ZERO:
        raise BacktestValidationError("initial_equity must be positive.")
    if simulations <= 0:
        raise BacktestValidationError("simulations must be positive.")
    if drawdown_limit < ZERO:
        raise BacktestValidationError("drawdown_limit must not be negative.")
    ordered_trades = tuple(sorted(trades, key=lambda trade: trade.closed_at))
    if not ordered_trades:
        raise BacktestValidationError("at least one trade is required.")

    rng = random.Random(seed)
    cagr_values: list[Decimal] = []
    drawdowns: list[Decimal] = []
    negative_results = 0
    above_limit = 0
    start = min(trade.opened_at for trade in ordered_trades)
    end = max(trade.closed_at for trade in ordered_trades)

    for _ in range(simulations):
        simulated = list(ordered_trades)
        rng.shuffle(simulated)
        equity_values = _equity_values_from_profits(
            initial_equity,
            tuple(trade.net_profit for trade in simulated),
        )
        ending_equity = equity_values[-1]
        max_drawdown = _max_drawdown_from_values(equity_values)
        cagr_values.append(_calculate_cagr(initial_equity, ending_equity, start, end))
        drawdowns.append(max_drawdown)
        if max_drawdown > drawdown_limit:
            above_limit += 1
        if ending_equity < initial_equity:
            negative_results += 1

    return MonteCarloSummary(
        number_of_simulations=simulations,
        seed=seed,
        sampling_mode="shuffle",
        percentile_cagr_5=_percentile(cagr_values, Decimal("0.05")),
        percentile_cagr_50=_percentile(cagr_values, Decimal("0.50")),
        percentile_cagr_95=_percentile(cagr_values, Decimal("0.95")),
        percentile_max_drawdown_5=_percentile(drawdowns, Decimal("0.05")),
        percentile_max_drawdown_50=_percentile(drawdowns, Decimal("0.50")),
        percentile_max_drawdown_95=_percentile(drawdowns, Decimal("0.95")),
        worst_simulated_drawdown=max(drawdowns),
        probability_drawdown_above_limit=Decimal(above_limit) / Decimal(simulations),
        probability_negative_result_after_costs=Decimal(negative_results) / Decimal(simulations),
    )


def build_walk_forward_report(
    windows: tuple[WalkForwardWindow, ...] | list[WalkForwardWindow],
    *,
    max_drawdown_limit: Decimal,
) -> WalkForwardReport:
    """Build an aggregated local mock walk-forward report."""
    if max_drawdown_limit < ZERO:
        raise BacktestValidationError("max_drawdown_limit must not be negative.")
    if not windows:
        raise BacktestValidationError("at least one walk-forward window is required.")

    results: list[WalkForwardWindowResult] = []
    for window in windows:
        trade_metrics = calculate_trade_metrics(window.trades)
        equity_metrics = calculate_equity_curve_metrics(window.equity_curve)
        profitable = trade_metrics.total_profit > ZERO and equity_metrics.total_return > ZERO
        results.append(
            WalkForwardWindowResult(
                window_id=window.window_id,
                train_window_days=(window.train_end - window.train_start).days,
                test_window_days=(window.test_end - window.test_start).days,
                trade_count=trade_metrics.trade_count,
                total_profit=trade_metrics.total_profit,
                total_return=equity_metrics.total_return,
                max_drawdown=equity_metrics.max_drawdown,
                profitable=profitable,
            )
        )

    profitable_windows = sum(1 for result in results if result.profitable)
    losing_windows = len(results) - profitable_windows
    aggregated_profit = sum((result.total_profit for result in results), ZERO)
    aggregated_max_drawdown = max(result.max_drawdown for result in results)
    conclusion: Conclusion = (
        "PASS"
        if (
            aggregated_profit > ZERO
            and profitable_windows > losing_windows
            and aggregated_max_drawdown <= max_drawdown_limit
        )
        else "RESEARCH_ONLY"
    )

    return WalkForwardReport(
        number_of_windows=len(results),
        train_window_days=round(
            sum(result.train_window_days for result in results) / len(results)
        ),
        test_window_days=round(sum(result.test_window_days for result in results) / len(results)),
        window_results=tuple(results),
        profitable_windows=profitable_windows,
        losing_windows=losing_windows,
        aggregated_profit=aggregated_profit,
        aggregated_max_drawdown=aggregated_max_drawdown,
        conclusion=conclusion,
    )


def calculate_buy_and_hold(
    prices: tuple[PricePoint, ...] | list[PricePoint],
    *,
    initial_cash: Decimal,
    fee_rate: Decimal = ZERO,
    slippage_rate: Decimal = ZERO,
) -> BuyAndHoldResult:
    """Calculate local buy-and-hold performance with optional costs."""
    if initial_cash <= ZERO:
        raise BacktestValidationError("initial_cash must be positive.")
    if fee_rate < ZERO or slippage_rate < ZERO:
        raise BacktestValidationError("fee_rate and slippage_rate must not be negative.")
    ordered_prices = _ordered_price_points(prices)
    if len(ordered_prices) < 2:
        raise BacktestValidationError("at least two price points are required.")

    first = ordered_prices[0]
    last = ordered_prices[-1]
    entry_fee = initial_cash * fee_rate
    entry_cash = initial_cash - entry_fee
    effective_entry_price = first.close * (ONE + slippage_rate)
    quantity = entry_cash / effective_entry_price
    effective_exit_price = last.close * (ONE - slippage_rate)
    gross_exit = quantity * effective_exit_price
    exit_fee = gross_exit * fee_rate
    ending_value = gross_exit - exit_fee

    return BuyAndHoldResult(
        starting_price=first.close,
        ending_price=last.close,
        quantity=quantity,
        ending_value=ending_value,
        total_profit=ending_value - initial_cash,
        total_return=ending_value / initial_cash - ONE,
        cagr=_calculate_cagr(initial_cash, ending_value, first.timestamp, last.timestamp),
    )


def build_offline_backtest_report(
    *,
    strategy_name: str,
    config_version: str,
    data_source_decision: str,
    pairs: tuple[str, ...],
    timeframe: str,
    generated_at: datetime,
    trades: tuple[TradeResult, ...],
    equity_curve: tuple[EquityPoint, ...],
    buy_and_hold_prices: tuple[PricePoint, ...],
    sensitivity_scenarios: tuple[CostScenario, ...],
    walk_forward_windows: tuple[WalkForwardWindow, ...],
    initial_equity: Decimal,
) -> OfflineBacktestReport:
    """Build a complete offline report from deterministic local inputs."""
    if any(pair not in SUPPORTED_PAIRS for pair in pairs):
        raise BacktestValidationError("report pairs must be limited to BTC/USD and ETH/USD.")
    trade_metrics = calculate_trade_metrics(trades)
    equity_metrics = calculate_equity_curve_metrics(equity_curve)
    exposure = calculate_exposure_ratio(
        trades,
        start=equity_curve[0].timestamp,
        end=equity_curve[-1].timestamp,
    )
    buy_and_hold = calculate_buy_and_hold(
        buy_and_hold_prices,
        initial_cash=initial_equity,
        fee_rate=Decimal("0.001"),
        slippage_rate=Decimal("0.0005"),
    )
    sensitivity = run_fee_slippage_sensitivity(
        trades,
        sensitivity_scenarios,
        initial_equity=initial_equity,
    )
    monte_carlo = monte_carlo_trade_order_resampling(
        trades,
        initial_equity=initial_equity,
        simulations=250,
        seed=20260621,
        drawdown_limit=Decimal("0.10"),
    )
    walk_forward = build_walk_forward_report(
        walk_forward_windows,
        max_drawdown_limit=Decimal("0.10"),
    )
    conclusion = _report_conclusion(equity_metrics, buy_and_hold, walk_forward)

    return OfflineBacktestReport(
        strategy_name=strategy_name,
        config_version=config_version,
        data_source_decision=data_source_decision,
        pairs=pairs,
        timeframe=timeframe,
        generated_at=_as_utc(generated_at),
        fee_model="mock roundtrip fee scenarios only; no exchange execution",
        slippage_model="mock local slippage scenarios only; no exchange execution",
        exposure=exposure,
        trades=trades,
        equity_curve=equity_curve,
        trade_metrics=trade_metrics,
        equity_metrics=equity_metrics,
        buy_and_hold=buy_and_hold,
        fee_slippage_sensitivity=sensitivity,
        monte_carlo=monte_carlo,
        walk_forward=walk_forward,
        conclusion=conclusion,
        local_acceptance_status="LOCAL_OFFLINE_PASS",
        deferred_status="DEFERRED_DOCKER_REQUIRED",
        deferred_items=DEFERRED_DOCKER_ITEMS,
    )


def build_sample_offline_report() -> OfflineBacktestReport:
    """Build the checked-in deterministic Phase 06 sample report."""
    initial_equity = Decimal("10000")
    trades = _sample_trades()
    return build_offline_backtest_report(
        strategy_name="CoinbaseTrendGuardV1",
        config_version="phase-06-local-offline-sample",
        data_source_decision=(
            "ADR-002 provisional: Coinbase Advanced Trade candidate raw source; "
            "Freqtrade engine candidate pending real parity and Docker checks."
        ),
        pairs=("BTC/USD", "ETH/USD"),
        timeframe="1h with 1d trend context",
        generated_at=datetime(2026, 6, 21, 13, 16, tzinfo=UTC),
        trades=trades,
        equity_curve=_equity_curve_from_trades(initial_equity, trades),
        buy_and_hold_prices=_sample_price_points(),
        sensitivity_scenarios=_sample_cost_scenarios(),
        walk_forward_windows=_sample_walk_forward_windows(initial_equity, trades),
        initial_equity=initial_equity,
    )


def render_markdown_report(report: OfflineBacktestReport) -> str:
    """Render a local/offline backtest report as markdown."""
    metrics = report.trade_metrics
    equity = report.equity_metrics
    lines = [
        "# Offline Backtest Validation Report",
        "",
        f"Strategy: `{report.strategy_name}`",
        f"Config version: `{report.config_version}`",
        f"Generated at: `{report.generated_at.isoformat()}`",
        f"Pairs: `{', '.join(report.pairs)}`",
        f"Timeframe: `{report.timeframe}`",
        f"Fee model: {report.fee_model}",
        f"Slippage model: {report.slippage_model}",
        f"Data source decision: {report.data_source_decision}",
        f"Local acceptance: `{report.local_acceptance_status}`",
        f"Deferred runtime status: `{report.deferred_status}`",
        f"Conclusion: `{report.conclusion}`",
        "",
        "## Core Metrics",
        "",
        f"- Total profit: {_format_money(metrics.total_profit)}",
        f"- CAGR: {_format_rate(equity.cagr)}",
        f"- Max drawdown: {_format_rate(equity.max_drawdown)}",
        f"- Sharpe: {_format_decimal(equity.sharpe)}",
        f"- Sortino: {_format_decimal(equity.sortino)}",
        f"- Profit factor: {_format_optional_decimal(metrics.profit_factor)}",
        f"- Win rate: {_format_rate(metrics.win_rate)}",
        f"- Average profit/trade: {_format_money(metrics.average_profit_per_trade)}",
        f"- Number of trades: {metrics.trade_count}",
        f"- Exposure: {_format_rate(report.exposure)}",
        f"- Max loss streak: {metrics.max_loss_streak}",
        f"- Best trade: {_format_money(metrics.best_trade_profit)}",
        f"- Worst trade: {_format_money(metrics.worst_trade_profit)}",
        f"- Buy-and-hold total return: {_format_rate(report.buy_and_hold.total_return)}",
        "",
        "## Fee And Slippage Sensitivity",
        "",
        "| Scenario | Fee rate | Slippage rate | Total profit | Total return | Win rate |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for result in report.fee_slippage_sensitivity:
        lines.append(
            "| "
            f"{result.name} | {_format_rate(result.fee_rate)} | "
            f"{_format_rate(result.slippage_rate)} | {_format_money(result.total_profit)} | "
            f"{_format_rate(result.total_return)} | {_format_rate(result.win_rate)} |"
        )

    lines.extend(
        [
            "",
            "## Monte Carlo",
            "",
            f"- Simulations: {report.monte_carlo.number_of_simulations}",
            f"- 5/50/95 percentile CAGR: {_format_rate(report.monte_carlo.percentile_cagr_5)} / "
            f"{_format_rate(report.monte_carlo.percentile_cagr_50)} / "
            f"{_format_rate(report.monte_carlo.percentile_cagr_95)}",
            "- 5/50/95 percentile max drawdown: "
            f"{_format_rate(report.monte_carlo.percentile_max_drawdown_5)} / "
            f"{_format_rate(report.monte_carlo.percentile_max_drawdown_50)} / "
            f"{_format_rate(report.monte_carlo.percentile_max_drawdown_95)}",
            "- Worst simulated drawdown: "
            f"{_format_rate(report.monte_carlo.worst_simulated_drawdown)}",
            "- Probability drawdown above limit: "
            f"{_format_rate(report.monte_carlo.probability_drawdown_above_limit)}",
            "- Probability negative result after costs: "
            f"{_format_rate(report.monte_carlo.probability_negative_result_after_costs)}",
            "",
            "## Walk Forward",
            "",
            f"- Windows: {report.walk_forward.number_of_windows}",
            f"- Train/test window days: {report.walk_forward.train_window_days} / "
            f"{report.walk_forward.test_window_days}",
            f"- Profitable/loss windows: {report.walk_forward.profitable_windows} / "
            f"{report.walk_forward.losing_windows}",
            f"- Aggregated profit: {_format_money(report.walk_forward.aggregated_profit)}",
            "- Aggregated max drawdown: "
            f"{_format_rate(report.walk_forward.aggregated_max_drawdown)}",
            f"- Walk-forward conclusion: `{report.walk_forward.conclusion}`",
            "",
            "## Enter Tag Aggregation",
            "",
        ]
    )
    for tag in metrics.enter_tag_breakdown:
        lines.append(
            f"- `{tag.enter_tag}`: trades={tag.trade_count}, "
            f"total_profit={_format_money(tag.total_profit)}"
        )

    lines.extend(
        [
            "",
            "## Monthly Returns",
            "",
        ]
    )
    for monthly_return in equity.monthly_returns:
        lines.append(
            f"- {monthly_return.year_month}: {_format_rate(monthly_return.return_rate)}"
        )

    lines.extend(
        [
            "",
            "## Deferred Runtime Items",
            "",
        ]
    )
    for item in report.deferred_items:
        lines.append(f"- `DEFERRED_DOCKER_REQUIRED`: {item}")

    lines.extend(
        [
            "",
            "## Disclaimer",
            "",
            report.disclaimer,
            "",
        ]
    )
    return "\n".join(lines)


def write_markdown_report(report: OfflineBacktestReport, output_path: Path) -> None:
    """Write a local/offline backtest report to markdown."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown_report(report), encoding="utf-8")


def write_json_report(report: OfflineBacktestReport, output_path: Path) -> None:
    """Write a local/offline backtest report to JSON."""
    _write_json_payload(report.to_json_dict(), output_path)


def write_report_bundle(
    report: OfflineBacktestReport,
    output_dir: Path,
    *,
    report_date: str,
) -> ReportBundlePaths:
    """Write the Phase 07 local report bundle and return all output paths."""
    if not report_date or "/" in report_date or "\\" in report_date or ".." in report_date:
        raise BacktestValidationError("report_date must be a safe filename prefix.")
    paths = ReportBundlePaths(
        strategy_summary=output_dir / f"{report_date}_strategy_summary.md",
        trades_csv=output_dir / f"{report_date}_trades.csv",
        metrics_json=output_dir / f"{report_date}_metrics.json",
        drawdown_csv=output_dir / f"{report_date}_drawdown.csv",
        walkforward_json=output_dir / f"{report_date}_walkforward.json",
        montecarlo_json=output_dir / f"{report_date}_montecarlo.json",
    )
    write_markdown_report(report, paths.strategy_summary)
    write_trades_csv(report, paths.trades_csv)
    write_metrics_json(report, paths.metrics_json)
    write_drawdown_csv(report, paths.drawdown_csv)
    write_walkforward_json(report, paths.walkforward_json)
    write_montecarlo_json(report, paths.montecarlo_json)
    return paths


def write_trades_csv(report: OfflineBacktestReport, output_path: Path) -> None:
    """Write closed local mock trades to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as csv_file:
        fieldnames = [
            "trade_id",
            "pair",
            "opened_at",
            "closed_at",
            "enter_tag",
            "entry_price",
            "exit_price",
            "quantity",
            "gross_profit",
            "total_costs",
            "net_profit",
            "return_rate",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for trade in report.trades:
            writer.writerow(
                {
                    "trade_id": trade.trade_id,
                    "pair": trade.pair,
                    "opened_at": trade.opened_at.isoformat(),
                    "closed_at": trade.closed_at.isoformat(),
                    "enter_tag": trade.enter_tag,
                    "entry_price": str(trade.entry_price),
                    "exit_price": str(trade.exit_price),
                    "quantity": str(trade.quantity),
                    "gross_profit": str(trade.gross_profit),
                    "total_costs": str(trade.total_costs),
                    "net_profit": str(trade.net_profit),
                    "return_rate": str(trade.return_rate),
                }
            )


def write_drawdown_csv(report: OfflineBacktestReport, output_path: Path) -> None:
    """Write the local mock drawdown curve to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as csv_file:
        fieldnames = ["timestamp", "equity", "drawdown"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for equity_point, drawdown_point in zip(
            report.equity_curve,
            report.equity_metrics.drawdown_curve,
            strict=True,
        ):
            writer.writerow(
                {
                    "timestamp": equity_point.timestamp.isoformat(),
                    "equity": str(equity_point.equity),
                    "drawdown": str(drawdown_point.drawdown),
                }
            )


def write_metrics_json(report: OfflineBacktestReport, output_path: Path) -> None:
    """Write the Phase 07 core metrics JSON payload."""
    payload = {
        "strategy_name": report.strategy_name,
        "config_version": report.config_version,
        "data_source_decision": report.data_source_decision,
        "pairs": report.pairs,
        "timeframe": report.timeframe,
        "fee_model": report.fee_model,
        "slippage_model": report.slippage_model,
        "number_of_trades": report.trade_metrics.trade_count,
        "max_drawdown": report.equity_metrics.max_drawdown,
        "buy_and_hold": report.buy_and_hold,
        "best_trade_profit": report.trade_metrics.best_trade_profit,
        "worst_trade_profit": report.trade_metrics.worst_trade_profit,
        "monthly_returns": report.equity_metrics.monthly_returns,
        "enter_tag_aggregation": report.trade_metrics.enter_tag_breakdown,
        "exposure": report.exposure,
        "conclusion": report.conclusion,
        "local_acceptance_status": report.local_acceptance_status,
        "deferred_status": report.deferred_status,
        "deferred_items": report.deferred_items,
        "disclaimer": report.disclaimer,
    }
    _write_json_payload(payload, output_path)


def write_walkforward_json(report: OfflineBacktestReport, output_path: Path) -> None:
    """Write the Phase 07 walk-forward JSON payload."""
    _write_json_payload(report.walk_forward, output_path)


def write_montecarlo_json(report: OfflineBacktestReport, output_path: Path) -> None:
    """Write the Phase 07 Monte Carlo JSON payload."""
    _write_json_payload(report.monte_carlo, output_path)


def _sample_trades() -> tuple[TradeResult, ...]:
    return (
        TradeResult(
            trade_id="mock-001",
            pair="BTC/USD",
            opened_at=datetime(2026, 1, 1, tzinfo=UTC),
            closed_at=datetime(2026, 1, 2, tzinfo=UTC),
            entry_price=Decimal("10000"),
            exit_price=Decimal("10600"),
            quantity=Decimal("0.10"),
            entry_fee=Decimal("1.00"),
            exit_fee=Decimal("1.06"),
            slippage_cost=Decimal("0.50"),
            enter_tag="trend_pullback",
        ),
        TradeResult(
            trade_id="mock-002",
            pair="ETH/USD",
            opened_at=datetime(2026, 1, 3, tzinfo=UTC),
            closed_at=datetime(2026, 1, 4, tzinfo=UTC),
            entry_price=Decimal("2000"),
            exit_price=Decimal("1920"),
            quantity=Decimal("1.00"),
            entry_fee=Decimal("2.00"),
            exit_fee=Decimal("1.92"),
            slippage_cost=Decimal("1.00"),
            enter_tag="trend_pullback",
        ),
        TradeResult(
            trade_id="mock-003",
            pair="BTC/USD",
            opened_at=datetime(2026, 1, 5, tzinfo=UTC),
            closed_at=datetime(2026, 1, 6, tzinfo=UTC),
            entry_price=Decimal("10500"),
            exit_price=Decimal("10800"),
            quantity=Decimal("0.08"),
            entry_fee=Decimal("0.84"),
            exit_fee=Decimal("0.864"),
            slippage_cost=Decimal("0.80"),
            enter_tag="volume_confirmed",
        ),
        TradeResult(
            trade_id="mock-004",
            pair="ETH/USD",
            opened_at=datetime(2026, 1, 8, tzinfo=UTC),
            closed_at=datetime(2026, 1, 9, tzinfo=UTC),
            entry_price=Decimal("1900"),
            exit_price=Decimal("2050"),
            quantity=Decimal("1.20"),
            entry_fee=Decimal("2.28"),
            exit_fee=Decimal("2.46"),
            slippage_cost=Decimal("1.20"),
            enter_tag="volume_confirmed",
        ),
        TradeResult(
            trade_id="mock-005",
            pair="BTC/USD",
            opened_at=datetime(2026, 1, 11, tzinfo=UTC),
            closed_at=datetime(2026, 1, 12, tzinfo=UTC),
            entry_price=Decimal("10800"),
            exit_price=Decimal("10300"),
            quantity=Decimal("0.05"),
            entry_fee=Decimal("0.54"),
            exit_fee=Decimal("0.515"),
            slippage_cost=Decimal("0.30"),
            enter_tag="trend_pullback",
        ),
        TradeResult(
            trade_id="mock-006",
            pair="ETH/USD",
            opened_at=datetime(2026, 1, 14, tzinfo=UTC),
            closed_at=datetime(2026, 1, 15, tzinfo=UTC),
            entry_price=Decimal("2050"),
            exit_price=Decimal("2140"),
            quantity=Decimal("0.90"),
            entry_fee=Decimal("1.845"),
            exit_fee=Decimal("1.926"),
            slippage_cost=Decimal("0.90"),
            enter_tag="trend_pullback",
        ),
    )


def _sample_price_points() -> tuple[PricePoint, ...]:
    return (
        PricePoint(datetime(2026, 1, 1, tzinfo=UTC), Decimal("10000")),
        PricePoint(datetime(2026, 1, 15, tzinfo=UTC), Decimal("10750")),
    )


def _sample_cost_scenarios() -> tuple[CostScenario, ...]:
    return (
        CostScenario("base_fee", Decimal("0.0010"), Decimal("0.0005")),
        CostScenario("worst_fee", Decimal("0.0030"), Decimal("0.0005")),
        CostScenario("slippage_low", Decimal("0.0010"), Decimal("0.0005")),
        CostScenario("slippage_medium", Decimal("0.0010"), Decimal("0.0015")),
        CostScenario("slippage_high", Decimal("0.0010"), Decimal("0.0030")),
    )


def _sample_walk_forward_windows(
    initial_equity: Decimal,
    trades: tuple[TradeResult, ...],
) -> tuple[WalkForwardWindow, ...]:
    return (
        _walk_forward_window(
            "mock-bull-window",
            datetime(2025, 12, 1, tzinfo=UTC),
            datetime(2025, 12, 15, tzinfo=UTC),
            datetime(2026, 1, 1, tzinfo=UTC),
            datetime(2026, 1, 7, tzinfo=UTC),
            initial_equity,
            trades[0:3],
        ),
        _walk_forward_window(
            "mock-sideways-window",
            datetime(2025, 12, 8, tzinfo=UTC),
            datetime(2025, 12, 22, tzinfo=UTC),
            datetime(2026, 1, 8, tzinfo=UTC),
            datetime(2026, 1, 13, tzinfo=UTC),
            initial_equity,
            trades[3:5],
        ),
        _walk_forward_window(
            "mock-out-of-sample-window",
            datetime(2025, 12, 15, tzinfo=UTC),
            datetime(2025, 12, 29, tzinfo=UTC),
            datetime(2026, 1, 14, tzinfo=UTC),
            datetime(2026, 1, 18, tzinfo=UTC),
            initial_equity,
            trades[5:6],
        ),
    )


def _walk_forward_window(
    window_id: str,
    train_start: datetime,
    train_end: datetime,
    test_start: datetime,
    test_end: datetime,
    initial_equity: Decimal,
    trades: tuple[TradeResult, ...],
) -> WalkForwardWindow:
    return WalkForwardWindow(
        window_id=window_id,
        train_start=train_start,
        train_end=train_end,
        test_start=test_start,
        test_end=test_end,
        trades=trades,
        equity_curve=_equity_curve_from_trades(initial_equity, trades),
    )


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise BacktestValidationError("datetime values must be timezone-aware.")
    return value.astimezone(UTC).replace(microsecond=0)


def _safe_ratio(numerator: Decimal, denominator: Decimal) -> Decimal:
    return ZERO if denominator == ZERO else numerator / denominator


def _build_enter_tag_breakdown(trades: tuple[TradeResult, ...]) -> tuple[EnterTagMetric, ...]:
    totals: dict[str, Decimal] = {}
    counts: dict[str, int] = {}
    for trade in trades:
        totals[trade.enter_tag] = totals.get(trade.enter_tag, ZERO) + trade.net_profit
        counts[trade.enter_tag] = counts.get(trade.enter_tag, 0) + 1
    return tuple(
        EnterTagMetric(enter_tag=tag, trade_count=counts[tag], total_profit=totals[tag])
        for tag in sorted(counts)
    )


def _calculate_max_loss_streak(profits: list[Decimal]) -> int:
    max_streak = 0
    current_streak = 0
    for profit in profits:
        if profit < ZERO:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    return max_streak


def _ordered_equity_points(
    equity_curve: tuple[EquityPoint, ...] | list[EquityPoint],
) -> tuple[EquityPoint, ...]:
    points = tuple(sorted(equity_curve, key=lambda point: point.timestamp))
    _reject_duplicate_timestamps(tuple(point.timestamp for point in points))
    return points


def _ordered_price_points(
    prices: tuple[PricePoint, ...] | list[PricePoint],
) -> tuple[PricePoint, ...]:
    points = tuple(sorted(prices, key=lambda point: point.timestamp))
    _reject_duplicate_timestamps(tuple(point.timestamp for point in points))
    return points


def _reject_duplicate_timestamps(timestamps: tuple[datetime, ...]) -> None:
    if len(set(timestamps)) != len(timestamps):
        raise BacktestValidationError("duplicate timestamps are not allowed.")


def _period_returns(points: tuple[EquityPoint, ...]) -> tuple[Decimal, ...]:
    returns: list[Decimal] = []
    for previous, current in zip(points, points[1:], strict=False):
        returns.append(current.equity / previous.equity - ONE)
    return tuple(returns)


def _calculate_cagr(
    starting_value: Decimal,
    ending_value: Decimal,
    start: datetime,
    end: datetime,
) -> Decimal:
    if starting_value <= ZERO:
        raise BacktestValidationError("starting_value must be positive.")
    if end <= start:
        return ZERO
    if ending_value <= ZERO:
        return Decimal("-1")
    duration_days = Decimal(str((end - start).total_seconds())) / Decimal("86400")
    years = duration_days / DAYS_PER_YEAR
    return _decimal_from_float(float(ending_value / starting_value) ** (1 / float(years)) - 1)


def _calculate_sharpe(
    returns: tuple[Decimal, ...],
    points: tuple[EquityPoint, ...],
) -> Decimal:
    if len(returns) < 2:
        return ZERO
    stddev = _stddev(returns)
    if stddev == ZERO:
        return ZERO
    return _mean(returns) / stddev * _periods_per_year(points).sqrt()


def _calculate_sortino(
    returns: tuple[Decimal, ...],
    points: tuple[EquityPoint, ...],
) -> Decimal:
    if len(returns) < 2:
        return ZERO
    downside = tuple(min(return_value, ZERO) for return_value in returns)
    downside_deviation = _stddev(downside)
    if downside_deviation == ZERO:
        return ZERO
    return _mean(returns) / downside_deviation * _periods_per_year(points).sqrt()


def _mean(values: tuple[Decimal, ...]) -> Decimal:
    return sum(values, ZERO) / Decimal(len(values))


def _stddev(values: tuple[Decimal, ...]) -> Decimal:
    if len(values) < 2:
        return ZERO
    average = _mean(values)
    variance = sum(((value - average) ** 2 for value in values), ZERO) / Decimal(len(values) - 1)
    return variance.sqrt()


def _periods_per_year(points: tuple[EquityPoint, ...]) -> Decimal:
    deltas = [
        Decimal(str((current.timestamp - previous.timestamp).total_seconds()))
        for previous, current in zip(points, points[1:], strict=False)
    ]
    if not deltas:
        return ONE
    average_delta = sum(deltas, ZERO) / Decimal(len(deltas))
    return SECONDS_PER_YEAR / average_delta


def _calculate_monthly_returns(points: tuple[EquityPoint, ...]) -> tuple[MonthlyReturn, ...]:
    by_month: dict[str, list[EquityPoint]] = {}
    for point in points:
        by_month.setdefault(point.timestamp.strftime("%Y-%m"), []).append(point)
    monthly_returns: list[MonthlyReturn] = []
    for year_month in sorted(by_month):
        month_points = sorted(by_month[year_month], key=lambda point: point.timestamp)
        start = month_points[0].equity
        end = month_points[-1].equity
        monthly_returns.append(MonthlyReturn(year_month, end / start - ONE))
    return tuple(monthly_returns)


def _apply_cost_scenario(trade: TradeResult, scenario: CostScenario) -> TradeResult:
    roundtrip_notional = trade.entry_notional + trade.exit_notional
    total_fee = roundtrip_notional * scenario.fee_rate
    slippage_cost = roundtrip_notional * scenario.slippage_rate
    return TradeResult(
        trade_id=trade.trade_id,
        pair=trade.pair,
        opened_at=trade.opened_at,
        closed_at=trade.closed_at,
        entry_price=trade.entry_price,
        exit_price=trade.exit_price,
        quantity=trade.quantity,
        entry_fee=total_fee / Decimal("2"),
        exit_fee=total_fee / Decimal("2"),
        slippage_cost=slippage_cost,
        enter_tag=trade.enter_tag,
    )


def _equity_values_from_profits(
    initial_equity: Decimal,
    profits: tuple[Decimal, ...],
) -> tuple[Decimal, ...]:
    values = [initial_equity]
    current = initial_equity
    for profit in profits:
        current += profit
        values.append(current)
    return tuple(values)


def _max_drawdown_from_values(values: tuple[Decimal, ...]) -> Decimal:
    peak = values[0]
    max_drawdown = ZERO
    for value in values:
        if value > peak:
            peak = value
        if peak > ZERO:
            max_drawdown = max(max_drawdown, (peak - value) / peak)
    return max_drawdown


def _percentile(values: list[Decimal], percentile: Decimal) -> Decimal:
    if not values:
        raise BacktestValidationError("percentile values must not be empty.")
    if percentile < ZERO or percentile > ONE:
        raise BacktestValidationError("percentile must be between 0 and 1.")
    sorted_values = sorted(values)
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = percentile * Decimal(len(sorted_values) - 1)
    lower_index = int(position)
    upper_index = min(lower_index + 1, len(sorted_values) - 1)
    weight = position - Decimal(lower_index)
    return sorted_values[lower_index] * (ONE - weight) + sorted_values[upper_index] * weight


def _equity_curve_from_trades(
    initial_equity: Decimal,
    trades: tuple[TradeResult, ...],
) -> tuple[EquityPoint, ...]:
    if initial_equity <= ZERO:
        raise BacktestValidationError("initial_equity must be positive.")
    start = min((trade.opened_at for trade in trades), default=datetime(2026, 1, 1, tzinfo=UTC))
    points = [EquityPoint(start, initial_equity)]
    current = initial_equity
    for trade in sorted(trades, key=lambda item: item.closed_at):
        current += trade.net_profit
        points.append(EquityPoint(trade.closed_at, current))
    return tuple(points)


def _report_conclusion(
    equity_metrics: EquityCurveMetrics,
    buy_and_hold: BuyAndHoldResult,
    walk_forward: WalkForwardReport,
) -> Conclusion:
    if equity_metrics.total_return <= ZERO:
        return "FAIL"
    if equity_metrics.total_return <= buy_and_hold.total_return:
        return "RESEARCH_ONLY"
    if walk_forward.conclusion != "PASS":
        return "RESEARCH_ONLY"
    return "PASS"


def _decimal_from_float(value: float) -> Decimal:
    return Decimal(str(round(value, 12)))


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if is_dataclass(value) and not isinstance(value, type):
        return {field.name: _to_jsonable(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, tuple | list):
        return [_to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _to_jsonable(item) for key, item in value.items()}
    return value


def _write_json_payload(payload: Any, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(_to_jsonable(payload), indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _format_money(value: Decimal) -> str:
    return f"${value.quantize(Decimal('0.01'))}"


def _format_rate(value: Decimal) -> str:
    return f"{(value * Decimal('100')).quantize(Decimal('0.01'))}%"


def _format_decimal(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.0001")))


def _format_optional_decimal(value: Decimal | None) -> str:
    if value is None:
        return "n/a"
    return _format_decimal(value)
