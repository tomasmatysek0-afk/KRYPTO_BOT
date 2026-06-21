"""Deterministic offline data parity checks for Coinbase/Freqtrade candles."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Literal, TypeAlias

Severity: TypeAlias = Literal["FAIL", "WARN"]
VolumeToleranceMode: TypeAlias = Literal["fail", "warn"]

SUPPORTED_PAIR_TO_PRODUCT = {
    "BTC/USD": "BTC-USD",
    "ETH/USD": "ETH-USD",
}
SUPPORTED_TIMEFRAMES = {
    "1h": timedelta(hours=1),
    "4h": timedelta(hours=4),
    "1d": timedelta(days=1),
}
PRICE_FIELDS = ("open", "high", "low", "close")


class DataParityError(ValueError):
    """Raised when data parity inputs are invalid or unsafe to compare."""


@dataclass(frozen=True, slots=True)
class Candle:
    """Closed or candidate OHLCV candle normalized to UTC."""

    pair: str
    timeframe: str
    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal

    def __post_init__(self) -> None:
        if self.pair not in SUPPORTED_PAIR_TO_PRODUCT:
            raise DataParityError(f"Unsupported pair for MVRS: {self.pair}")
        if self.timeframe not in SUPPORTED_TIMEFRAMES:
            raise DataParityError(f"Unsupported timeframe: {self.timeframe}")
        if self.timestamp.tzinfo is None:
            raise DataParityError("Candle timestamp must be timezone-aware.")
        timestamp_utc = self.timestamp.astimezone(UTC).replace(microsecond=0)
        object.__setattr__(self, "timestamp", timestamp_utc)


@dataclass(frozen=True, slots=True)
class ParityConfig:
    """Configurable parity tolerances."""

    price_tolerance: Decimal = Decimal("0")
    volume_tolerance: Decimal = Decimal("0")
    volume_tolerance_mode: VolumeToleranceMode = "fail"

    def __post_init__(self) -> None:
        if self.price_tolerance < 0:
            raise DataParityError("price_tolerance must not be negative.")
        if self.volume_tolerance < 0:
            raise DataParityError("volume_tolerance must not be negative.")
        if self.volume_tolerance_mode not in {"fail", "warn"}:
            raise DataParityError("volume_tolerance_mode must be 'fail' or 'warn'.")


@dataclass(frozen=True, slots=True)
class ParityIssue:
    """Single data parity finding."""

    severity: Severity
    code: str
    message: str
    pair: str
    timeframe: str
    timestamp: datetime | None = None
    field: str | None = None


@dataclass(frozen=True, slots=True)
class ParityResult:
    """Result of comparing two candle streams."""

    reference_source: str
    candidate_source: str
    pair: str
    timeframe: str
    compared_candles: int
    issues: tuple[ParityIssue, ...] = field(default_factory=tuple)

    @property
    def passed(self) -> bool:
        """Return true only when the result has no FAIL issues."""
        return not any(issue.severity == "FAIL" for issue in self.issues)

    @property
    def failures(self) -> tuple[ParityIssue, ...]:
        """Return all FAIL issues."""
        return tuple(issue for issue in self.issues if issue.severity == "FAIL")

    @property
    def warnings(self) -> tuple[ParityIssue, ...]:
        """Return all WARN issues."""
        return tuple(issue for issue in self.issues if issue.severity == "WARN")


def coinbase_product_id(pair: str) -> str:
    """Map a supported project pair to a Coinbase Advanced Trade product id."""
    try:
        return SUPPORTED_PAIR_TO_PRODUCT[pair]
    except KeyError as exc:
        raise DataParityError(f"Unsupported pair for Coinbase mapping: {pair}") from exc


def is_closed_candle(candle: Candle, as_of: datetime) -> bool:
    """Return true when a candle is fully closed at the supplied UTC instant."""
    as_of_utc = _as_utc(as_of)
    return candle.timestamp + SUPPORTED_TIMEFRAMES[candle.timeframe] <= as_of_utc


def compare_candles(
    reference: list[Candle] | tuple[Candle, ...],
    candidate: list[Candle] | tuple[Candle, ...],
    *,
    as_of: datetime,
    config: ParityConfig | None = None,
    reference_source: str = "coinbase_advanced",
    candidate_source: str = "freqtrade_ccxt",
) -> ParityResult:
    """Compare two candle streams after dropping unclosed candles."""
    parity_config = config or ParityConfig()
    reference_closed = _closed_only(reference, as_of)
    candidate_closed = _closed_only(candidate, as_of)
    pair, timeframe = _resolve_pair_timeframe(reference_closed, candidate_closed)
    issues: list[ParityIssue] = []

    reference_by_timestamp = _index_by_timestamp(reference_closed, pair, timeframe, issues)
    candidate_by_timestamp = _index_by_timestamp(candidate_closed, pair, timeframe, issues)

    reference_timestamps = set(reference_by_timestamp)
    candidate_timestamps = set(candidate_by_timestamp)
    missing_timestamps = sorted(reference_timestamps - candidate_timestamps)
    unexpected_timestamps = sorted(candidate_timestamps - reference_timestamps)

    if missing_timestamps and unexpected_timestamps and len(reference_timestamps) == len(
        candidate_timestamps
    ):
        issues.append(
            ParityIssue(
                severity="FAIL",
                code="shifted_timestamp",
                message="Candidate timestamps are shifted relative to reference timestamps.",
                pair=pair,
                timeframe=timeframe,
            )
        )

    for timestamp in missing_timestamps:
        issues.append(
            ParityIssue(
                severity="FAIL",
                code="missing_candidate_candle",
                message="Reference candle is missing from candidate data.",
                pair=pair,
                timeframe=timeframe,
                timestamp=timestamp,
            )
        )

    for timestamp in unexpected_timestamps:
        issues.append(
            ParityIssue(
                severity="FAIL",
                code="unexpected_candidate_candle",
                message="Candidate data contains a candle not present in reference data.",
                pair=pair,
                timeframe=timeframe,
                timestamp=timestamp,
            )
        )

    compared_candles = 0
    for timestamp in sorted(reference_timestamps & candidate_timestamps):
        reference_candle = reference_by_timestamp[timestamp]
        candidate_candle = candidate_by_timestamp[timestamp]
        compared_candles += 1
        issues.extend(_compare_ohlcv(reference_candle, candidate_candle, parity_config))

    if compared_candles == 0:
        issues.append(
            ParityIssue(
                severity="FAIL",
                code="no_comparable_closed_candles",
                message="No matching closed candles were available for comparison.",
                pair=pair,
                timeframe=timeframe,
            )
        )

    return ParityResult(
        reference_source=reference_source,
        candidate_source=candidate_source,
        pair=pair,
        timeframe=timeframe,
        compared_candles=compared_candles,
        issues=tuple(issues),
    )


def aggregate_1h_to_4h(
    candles: list[Candle] | tuple[Candle, ...],
    *,
    as_of: datetime,
) -> tuple[Candle, ...]:
    """Aggregate complete closed 1h candles into deterministic 4h candles."""
    closed_candles = sorted(_closed_only(candles, as_of), key=lambda candle: candle.timestamp)
    if not closed_candles:
        return ()
    pair = closed_candles[0].pair
    if any(candle.pair != pair for candle in closed_candles):
        raise DataParityError("Cannot aggregate mixed pairs.")
    if any(candle.timeframe != "1h" for candle in closed_candles):
        raise DataParityError("Only 1h candles can be aggregated to 4h.")

    grouped: dict[datetime, list[Candle]] = {}
    for candle in closed_candles:
        group_start = candle.timestamp.replace(
            hour=(candle.timestamp.hour // 4) * 4,
            minute=0,
            second=0,
            microsecond=0,
        )
        grouped.setdefault(group_start, []).append(candle)

    aggregates: list[Candle] = []
    for group_start, group_candles in sorted(grouped.items()):
        expected_timestamps = [group_start + timedelta(hours=offset) for offset in range(4)]
        actual_timestamps = [candle.timestamp for candle in group_candles]
        if actual_timestamps != expected_timestamps:
            continue
        aggregates.append(
            Candle(
                pair=pair,
                timeframe="4h",
                timestamp=group_start,
                open=group_candles[0].open,
                high=max(candle.high for candle in group_candles),
                low=min(candle.low for candle in group_candles),
                close=group_candles[-1].close,
                volume=sum((candle.volume for candle in group_candles), Decimal("0")),
            )
        )
    return tuple(aggregates)


def render_markdown_report(result: ParityResult) -> str:
    """Render a parity result as a compact markdown report."""
    status = "PASS" if result.passed else "FAIL"
    lines = [
        "# Data Parity Report",
        "",
        f"Status: {status}",
        f"Pair: `{result.pair}`",
        f"Timeframe: `{result.timeframe}`",
        f"Reference source: `{result.reference_source}`",
        f"Candidate source: `{result.candidate_source}`",
        f"Compared closed candles: {result.compared_candles}",
        "",
        "## Issues",
        "",
    ]
    if not result.issues:
        lines.append("- None.")
    for issue in result.issues:
        timestamp = issue.timestamp.isoformat() if issue.timestamp else "n/a"
        field = issue.field or "n/a"
        lines.append(
            f"- {issue.severity} `{issue.code}` timestamp={timestamp} "
            f"field={field}: {issue.message}"
        )
    lines.append("")
    lines.append("Docker/Freqtrade runtime checks may still be DEFERRED_DOCKER_REQUIRED.")
    return "\n".join(lines)


def write_markdown_report(result: ParityResult, output_path: Path) -> None:
    """Write a parity result markdown report to disk."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown_report(result), encoding="utf-8")


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise DataParityError("Datetime must be timezone-aware.")
    return value.astimezone(UTC).replace(microsecond=0)


def _closed_only(candles: list[Candle] | tuple[Candle, ...], as_of: datetime) -> tuple[Candle, ...]:
    return tuple(candle for candle in candles if is_closed_candle(candle, as_of))


def _resolve_pair_timeframe(
    reference: tuple[Candle, ...],
    candidate: tuple[Candle, ...],
) -> tuple[str, str]:
    all_candles = reference + candidate
    if not all_candles:
        return "BTC/USD", "1h"
    pair = all_candles[0].pair
    timeframe = all_candles[0].timeframe
    if any(candle.pair != pair for candle in all_candles):
        raise DataParityError("Cannot compare mixed pairs.")
    if any(candle.timeframe != timeframe for candle in all_candles):
        raise DataParityError("Cannot compare mixed timeframes.")
    return pair, timeframe


def _index_by_timestamp(
    candles: tuple[Candle, ...],
    pair: str,
    timeframe: str,
    issues: list[ParityIssue],
) -> dict[datetime, Candle]:
    indexed: dict[datetime, Candle] = {}
    for candle in candles:
        if candle.timestamp in indexed:
            issues.append(
                ParityIssue(
                    severity="FAIL",
                    code="duplicate_timestamp",
                    message="Duplicate candle timestamp found.",
                    pair=pair,
                    timeframe=timeframe,
                    timestamp=candle.timestamp,
                )
            )
        indexed[candle.timestamp] = candle
    return indexed


def _compare_ohlcv(
    reference: Candle,
    candidate: Candle,
    config: ParityConfig,
) -> list[ParityIssue]:
    issues: list[ParityIssue] = []
    for field_name in PRICE_FIELDS:
        reference_value = getattr(reference, field_name)
        candidate_value = getattr(candidate, field_name)
        if abs(reference_value - candidate_value) > config.price_tolerance:
            issues.append(
                ParityIssue(
                    severity="FAIL",
                    code="ohlc_mismatch",
                    message=(
                        f"Reference {reference_value} and candidate {candidate_value} "
                        f"differ above tolerance {config.price_tolerance}."
                    ),
                    pair=reference.pair,
                    timeframe=reference.timeframe,
                    timestamp=reference.timestamp,
                    field=field_name,
                )
            )

    if abs(reference.volume - candidate.volume) > config.volume_tolerance:
        severity: Severity = "FAIL" if config.volume_tolerance_mode == "fail" else "WARN"
        issues.append(
            ParityIssue(
                severity=severity,
                code="volume_mismatch",
                message=(
                    f"Reference {reference.volume} and candidate {candidate.volume} "
                    f"differ above tolerance {config.volume_tolerance}."
                ),
                pair=reference.pair,
                timeframe=reference.timeframe,
                timestamp=reference.timestamp,
                field="volume",
            )
        )
    return issues
