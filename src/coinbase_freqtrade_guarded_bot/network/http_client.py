"""Bounded retry HTTP client primitives for deterministic network behavior."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Protocol


class HttpClientError(RuntimeError):
    """Raised when an HTTP request cannot complete within retry policy."""


@dataclass(frozen=True, slots=True)
class HttpRequest:
    """HTTP request passed to an injected transport."""

    method: str
    url: str
    headers: Mapping[str, str] = field(default_factory=dict)
    body: bytes | None = None


@dataclass(frozen=True, slots=True)
class HttpResponse:
    """HTTP response returned by an injected transport."""

    status_code: int
    body: bytes
    headers: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """Retry and backoff settings."""

    max_attempts: int = 3
    base_delay_seconds: float = 0.25
    max_delay_seconds: float = 5.0
    retry_statuses: tuple[int, ...] = (429, 503)

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise HttpClientError("max_attempts must be at least 1.")
        if self.base_delay_seconds < 0:
            raise HttpClientError("base_delay_seconds must not be negative.")
        if self.max_delay_seconds < self.base_delay_seconds:
            raise HttpClientError("max_delay_seconds must be >= base_delay_seconds.")


class HttpTransport(Protocol):
    """Callable transport used by HttpClient."""

    def __call__(self, request: HttpRequest, timeout_seconds: float) -> HttpResponse:
        """Send an HTTP request and return a response."""


Sleeper = Callable[[float], None]


class HttpClient:
    """HTTP client with bounded retries, timeout propagation, and backoff."""

    def __init__(
        self,
        *,
        transport: HttpTransport,
        retry_policy: RetryPolicy | None = None,
        timeout_seconds: float = 10.0,
        sleeper: Sleeper | None = None,
    ) -> None:
        """Create a client using an injected transport and optional sleeper."""
        if timeout_seconds <= 0:
            raise HttpClientError("timeout_seconds must be positive.")
        self._transport = transport
        self._retry_policy = retry_policy or RetryPolicy()
        self._timeout_seconds = timeout_seconds
        self._sleeper = sleeper or _noop_sleep

    def send(self, request: HttpRequest) -> HttpResponse:
        """Send a request and retry bounded transient failures."""
        last_timeout: TimeoutError | None = None
        for attempt in range(1, self._retry_policy.max_attempts + 1):
            try:
                response = self._transport(request, self._timeout_seconds)
            except TimeoutError as exc:
                last_timeout = exc
                if attempt == self._retry_policy.max_attempts:
                    raise HttpClientError("HTTP request timed out after retries.") from exc
                self._sleep_before_retry(attempt, None)
                continue

            if response.status_code not in self._retry_policy.retry_statuses:
                return response
            if attempt == self._retry_policy.max_attempts:
                raise HttpClientError(
                    f"HTTP {response.status_code} after "
                    f"{self._retry_policy.max_attempts} attempts."
                )
            self._sleep_before_retry(attempt, response)

        raise HttpClientError("HTTP request failed.") from last_timeout

    def _sleep_before_retry(self, attempt: int, response: HttpResponse | None) -> None:
        retry_after = _retry_after_seconds(response)
        delay = retry_after if retry_after is not None else self._backoff_seconds(attempt)
        self._sleeper(delay)

    def _backoff_seconds(self, attempt: int) -> float:
        delay = self._retry_policy.base_delay_seconds * (2 ** (attempt - 1))
        return min(delay, self._retry_policy.max_delay_seconds)


def _retry_after_seconds(response: HttpResponse | None) -> float | None:
    if response is None:
        return None
    raw_retry_after = response.headers.get("Retry-After")
    if raw_retry_after is None:
        return None
    try:
        parsed = float(raw_retry_after)
    except ValueError:
        return None
    if parsed < 0:
        return None
    return parsed


def _noop_sleep(_: float) -> None:
    return None
