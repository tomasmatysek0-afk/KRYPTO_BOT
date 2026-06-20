# reconciliation

## Purpose

Track order and fill reconciliation rules.

## Current conclusions

An unreconciled or unknown order status must block further intent processing.

## Findings

### 2026-06-20 - Bootstrap
Source:
- CODEX_MASTER_PLAN.md

Summary:
Reconciliation is required before live readiness and must fail closed on mismatch or unknown status.

Decision impact:
No live order path may be added before reconciliation exists and passes tests.

Open questions:
- None for Phase 00.
