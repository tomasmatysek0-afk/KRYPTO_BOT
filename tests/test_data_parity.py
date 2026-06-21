"""Deterministic tests for data parity and HTTP retry behavior."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from coinbase_freqtrade_guarded_bot.guard_layer.data_parity import (
    Candle,
    DataParityError,
    ParityConfig,
    aggregate_1h_to_4h,
    coinbase_product_id,
    compare_candles,
    render_markdown_report,
    write_markdown_report,
)
from coinbase_freqtrade_guarded_bot.network.http_client import (
    HttpClient,
    HttpClientError,
    HttpRequest,
    HttpResponse,
    RetryPolicy,
)


def _candle(
    hour: int,
    *,
    close: str = "105",
    volume: str = "12.5",
    timeframe: str = "1h",
    pair: str = "BTC/USD",
) -> Candle:
    return Candle(
        pair=pair,
        timeframe=timeframe,
        timestamp=datetime(2026, 1, 1, hour, tzinfo=UTC),
        open=Decimal("100"),
        high=Decimal("110"),
        low=Decimal("90"),
        close=Decimal(close),
        volume=Decimal(volume),
    )


def test_coinbase_product_mapping_allows_only_mvrs_pairs() -> None:
    """Only BTC/USD and ETH/USD map to Coinbase product ids."""
    assert coinbase_product_id("BTC/USD") == "BTC-USD"
    assert coinbase_product_id("ETH/USD") == "ETH-USD"

    with pytest.raises(DataParityError):
        coinbase_product_id("DOGE/USD")


def test_invalid_candle_and_config_inputs_fail_closed() -> None:
    """Invalid parity inputs raise domain-specific exceptions."""
    with pytest.raises(DataParityError):
        _candle(0, pair="DOGE/USD")
    with pytest.raises(DataParityError):
        _candle(0, timeframe="5m")
    with pytest.raises(DataParityError):
        Candle(
            pair="BTC/USD",
            timeframe="1h",
            timestamp=datetime(2026, 1, 1),
            open=Decimal("1"),
            high=Decimal("1"),
            low=Decimal("1"),
            close=Decimal("1"),
            volume=Decimal("1"),
        )
    with pytest.raises(DataParityError):
        ParityConfig(price_tolerance=Decimal("-0.1"))
    with pytest.raises(DataParityError):
        ParityConfig(volume_tolerance=Decimal("-0.1"))
    with pytest.raises(DataParityError):
        ParityConfig(volume_tolerance_mode="skip")  # type: ignore[arg-type]


def test_compare_candles_passes_for_matching_closed_candles() -> None:
    """Matching closed candles pass without issues."""
    as_of = datetime(2026, 1, 1, 2, tzinfo=UTC)
    candle = _candle(0)

    result = compare_candles([candle], [candle], as_of=as_of)

    assert result.passed
    assert result.compared_candles == 1
    assert result.issues == ()
    assert "Status: PASS" in render_markdown_report(result)


def test_compare_empty_closed_data_fails() -> None:
    """No comparable closed candles fails closed."""
    result = compare_candles([], [], as_of=datetime(2026, 1, 1, tzinfo=UTC))

    assert not result.passed
    assert result.failures[0].code == "no_comparable_closed_candles"


def test_compare_rejects_mixed_pairs_and_timeframes() -> None:
    """Mixed pair or timeframe streams are unsafe to compare."""
    as_of = datetime(2026, 1, 2, tzinfo=UTC)

    with pytest.raises(DataParityError):
        compare_candles([_candle(0)], [_candle(0, pair="ETH/USD")], as_of=as_of)
    with pytest.raises(DataParityError):
        compare_candles([_candle(0)], [_candle(0, timeframe="1d")], as_of=as_of)


def test_duplicate_timestamp_fails() -> None:
    """Duplicate timestamps fail rather than silently picking one candle."""
    as_of = datetime(2026, 1, 1, 2, tzinfo=UTC)

    result = compare_candles([_candle(0), _candle(0)], [_candle(0)], as_of=as_of)

    assert not result.passed
    assert "duplicate_timestamp" in {issue.code for issue in result.failures}


def test_compare_candles_supports_eth_usd_daily_timeframe() -> None:
    """ETH/USD 1d candles are supported for the trend filter."""
    as_of = datetime(2026, 1, 3, tzinfo=UTC)
    candle = Candle(
        pair="ETH/USD",
        timeframe="1d",
        timestamp=datetime(2026, 1, 1, tzinfo=UTC),
        open=Decimal("1000"),
        high=Decimal("1100"),
        low=Decimal("900"),
        close=Decimal("1050"),
        volume=Decimal("25"),
    )

    result = compare_candles([candle], [candle], as_of=as_of)

    assert result.passed
    assert result.pair == "ETH/USD"
    assert result.timeframe == "1d"


def test_compare_candles_ignores_unclosed_current_candle() -> None:
    """Unclosed current candles are ignored before comparison."""
    as_of = datetime(2026, 1, 1, 1, 30, tzinfo=UTC)
    closed = _candle(0)
    unclosed_reference = _candle(1, close="999")
    unclosed_candidate = _candle(1, close="1")

    result = compare_candles(
        [closed, unclosed_reference],
        [closed, unclosed_candidate],
        as_of=as_of,
    )

    assert result.passed
    assert result.compared_candles == 1


def test_missing_candle_fails() -> None:
    """Missing candidate candles fail closed."""
    as_of = datetime(2026, 1, 1, 3, tzinfo=UTC)

    result = compare_candles([_candle(0), _candle(1)], [_candle(0)], as_of=as_of)

    assert not result.passed
    assert "missing_candidate_candle" in {issue.code for issue in result.failures}


def test_shifted_timestamp_fails() -> None:
    """Shifted candidate timestamps are explicit failures."""
    as_of = datetime(2026, 1, 1, 3, tzinfo=UTC)

    result = compare_candles([_candle(0)], [_candle(1)], as_of=as_of)

    assert not result.passed
    assert "shifted_timestamp" in {issue.code for issue in result.failures}


def test_ohlc_difference_above_tolerance_fails() -> None:
    """OHLC mismatches above configured tolerance fail."""
    as_of = datetime(2026, 1, 1, 2, tzinfo=UTC)
    reference = _candle(0, close="105.00")
    candidate = _candle(0, close="105.03")

    result = compare_candles(
        [reference],
        [candidate],
        as_of=as_of,
        config=ParityConfig(price_tolerance=Decimal("0.01")),
    )

    assert not result.passed
    assert any(issue.field == "close" for issue in result.failures)


def test_ohlc_difference_inside_tolerance_passes() -> None:
    """OHLC mismatches inside configured tolerance pass."""
    as_of = datetime(2026, 1, 1, 2, tzinfo=UTC)
    reference = _candle(0, close="105.00")
    candidate = _candle(0, close="105.03")

    result = compare_candles(
        [reference],
        [candidate],
        as_of=as_of,
        config=ParityConfig(price_tolerance=Decimal("0.05")),
    )

    assert result.passed


def test_volume_tolerance_can_warn_or_fail() -> None:
    """Volume mismatches follow configured WARN/FAIL behavior."""
    as_of = datetime(2026, 1, 1, 2, tzinfo=UTC)
    reference = _candle(0, volume="10")
    candidate = _candle(0, volume="11")

    warn_result = compare_candles(
        [reference],
        [candidate],
        as_of=as_of,
        config=ParityConfig(volume_tolerance=Decimal("0.1"), volume_tolerance_mode="warn"),
    )
    fail_result = compare_candles(
        [reference],
        [candidate],
        as_of=as_of,
        config=ParityConfig(volume_tolerance=Decimal("0.1"), volume_tolerance_mode="fail"),
    )

    assert warn_result.passed
    assert warn_result.warnings[0].code == "volume_mismatch"
    assert not fail_result.passed
    assert fail_result.failures[0].code == "volume_mismatch"


def test_aggregate_1h_to_4h_uses_complete_closed_groups_only() -> None:
    """Four consecutive closed 1h candles aggregate into one 4h candle."""
    as_of = datetime(2026, 1, 1, 4, 30, tzinfo=UTC)
    candles = [
        _candle(0, close="101", volume="1"),
        _candle(1, close="102", volume="2"),
        _candle(2, close="103", volume="3"),
        _candle(3, close="104", volume="4"),
        _candle(4, close="999", volume="100"),
    ]

    aggregates = aggregate_1h_to_4h(candles, as_of=as_of)

    assert len(aggregates) == 1
    aggregate = aggregates[0]
    assert aggregate.timeframe == "4h"
    assert aggregate.timestamp == datetime(2026, 1, 1, 0, tzinfo=UTC)
    assert aggregate.open == Decimal("100")
    assert aggregate.high == Decimal("110")
    assert aggregate.low == Decimal("90")
    assert aggregate.close == Decimal("104")
    assert aggregate.volume == Decimal("10")


def test_aggregate_1h_to_4h_handles_incomplete_and_invalid_inputs() -> None:
    """Aggregation skips incomplete groups and rejects unsafe inputs."""
    as_of = datetime(2026, 1, 1, 4, tzinfo=UTC)

    assert aggregate_1h_to_4h([], as_of=as_of) == ()
    assert aggregate_1h_to_4h([_candle(0), _candle(1), _candle(2)], as_of=as_of) == ()

    with pytest.raises(DataParityError):
        aggregate_1h_to_4h([_candle(0), _candle(1, pair="ETH/USD")], as_of=as_of)
    with pytest.raises(DataParityError):
        aggregate_1h_to_4h([_candle(0, timeframe="4h")], as_of=as_of)


def test_render_and_write_failed_markdown_report(tmp_path: Path) -> None:
    """Failed reports include issue details and can be written to disk."""
    as_of = datetime(2026, 1, 1, 3, tzinfo=UTC)
    result = compare_candles([_candle(0)], [_candle(1)], as_of=as_of)
    report_path = tmp_path / "parity_report.md"

    write_markdown_report(result, report_path)
    report_text = report_path.read_text(encoding="utf-8")

    assert "Status: FAIL" in report_text
    assert "shifted_timestamp" in report_text
    assert "timestamp=n/a" in report_text


def test_http_client_retries_503_then_returns_success() -> None:
    """HTTP 503 responses use bounded backoff before success."""
    responses = [HttpResponse(503, b""), HttpResponse(200, b"ok")]
    sleeps: list[float] = []

    client = HttpClient(
        transport=lambda _request, _timeout: responses.pop(0),
        retry_policy=RetryPolicy(max_attempts=3, base_delay_seconds=1),
        sleeper=sleeps.append,
    )

    response = client.send(HttpRequest("GET", "https://example.test"))

    assert response.status_code == 200
    assert sleeps == [1]


def test_http_client_retries_429_with_retry_after() -> None:
    """HTTP 429 honors numeric Retry-After before retrying."""
    responses = [
        HttpResponse(429, b"", headers={"Retry-After": "2.5"}),
        HttpResponse(200, b"ok"),
    ]
    sleeps: list[float] = []
    client = HttpClient(
        transport=lambda _request, _timeout: responses.pop(0),
        retry_policy=RetryPolicy(max_attempts=2, base_delay_seconds=1),
        sleeper=sleeps.append,
    )

    response = client.send(HttpRequest("GET", "https://example.test"))

    assert response.status_code == 200
    assert sleeps == [2.5]


def test_http_client_retries_timeout_with_exponential_backoff() -> None:
    """Timeouts are retried with exponential backoff."""
    attempts = 0
    sleeps: list[float] = []

    def transport(_request: HttpRequest, _timeout: float) -> HttpResponse:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise TimeoutError("timed out")
        return HttpResponse(200, b"ok")

    client = HttpClient(
        transport=transport,
        retry_policy=RetryPolicy(max_attempts=3, base_delay_seconds=0.5),
        sleeper=sleeps.append,
    )

    response = client.send(HttpRequest("GET", "https://example.test"))

    assert response.status_code == 200
    assert sleeps == [0.5, 1.0]


def test_http_client_exhausts_retryable_statuses() -> None:
    """Retryable status exhaustion raises a domain exception."""
    client = HttpClient(
        transport=lambda _request, _timeout: HttpResponse(503, b""),
        retry_policy=RetryPolicy(max_attempts=2, base_delay_seconds=0),
        sleeper=lambda _delay: None,
    )

    with pytest.raises(HttpClientError):
        client.send(HttpRequest("GET", "https://example.test"))


def test_http_client_retries_timeout_until_exhaustion() -> None:
    """Timeout exhaustion raises a domain exception."""
    client = HttpClient(
        transport=lambda _request, _timeout: (_ for _ in ()).throw(TimeoutError("timed out")),
        retry_policy=RetryPolicy(max_attempts=2, base_delay_seconds=0),
        sleeper=lambda _delay: None,
    )

    with pytest.raises(HttpClientError):
        client.send(HttpRequest("GET", "https://example.test"))


def test_http_client_validates_retry_policy_and_timeout_settings() -> None:
    """Invalid retry and timeout settings fail during construction."""
    with pytest.raises(HttpClientError):
        RetryPolicy(max_attempts=0)
    with pytest.raises(HttpClientError):
        RetryPolicy(base_delay_seconds=-1)
    with pytest.raises(HttpClientError):
        RetryPolicy(base_delay_seconds=2, max_delay_seconds=1)
    with pytest.raises(HttpClientError):
        HttpClient(
            transport=lambda _request, _timeout: HttpResponse(200, b"ok"),
            timeout_seconds=0,
        )


def test_http_client_ignores_invalid_retry_after_and_caps_backoff() -> None:
    """Invalid Retry-After values fall back to capped exponential backoff."""
    responses = [
        HttpResponse(429, b"", headers={"Retry-After": "not-a-number"}),
        HttpResponse(429, b"", headers={"Retry-After": "-1"}),
        HttpResponse(200, b"ok"),
    ]
    sleeps: list[float] = []
    client = HttpClient(
        transport=lambda _request, _timeout: responses.pop(0),
        retry_policy=RetryPolicy(max_attempts=3, base_delay_seconds=10, max_delay_seconds=15),
        sleeper=sleeps.append,
    )

    response = client.send(HttpRequest("GET", "https://example.test"))

    assert response.status_code == 200
    assert sleeps == [10, 15]


def test_mock_data_parity_report_exists() -> None:
    """Phase 03b includes a checked-in mock report artifact."""
    report_path = (
        Path(__file__).resolve().parents[1]
        / "reports"
        / "data_parity"
        / "2026-06-21_mock_parity_report.md"
    )

    assert report_path.exists()
    assert "Status: PASS" in report_path.read_text(encoding="utf-8")
