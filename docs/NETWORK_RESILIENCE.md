# Network Resilience

## Purpose

Define the network behavior required before Coinbase, CCXT, Freqtrade API, or any external source is used.

## Current Phase

Phase 00b does not implement network clients and does not perform network calls in unit tests.

## Future Rules

- Every HTTP/API call must have an explicit timeout.
- Retries must have bounded attempts and a total deadline.
- HTTP 429 must respect `Retry-After` if available.
- HTTP 5xx and temporary network errors use bounded exponential backoff with jitter.
- HTTP 401/403 is not retried indefinitely.
- Unit tests must mock network clients.
- Network calls must not run during import.

## Dependency Note

`tenacity` is deferred until a later network resilience phase and requires dependency review before use.
