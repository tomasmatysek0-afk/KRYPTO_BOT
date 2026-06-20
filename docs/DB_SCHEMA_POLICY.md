# DB Schema Policy

## Purpose

Protect local audit, dry-run, and tax records from silent schema damage.

## Current Phase

Phase 00b does not create runtime databases.

## Rules

- Runtime DB files must not be committed.
- SQLite schemas must include a schema version or equivalent metadata once introduced.
- Every schema change needs a migration note.
- Disposable test or replayable MVRS dry-run DBs may be reset only with a LOG entry.
- Valuable dry-run or live data requires backup before migration.
- Append-only JSONL audit files are not destructively migrated.

## Deferred Work

Migration code and tests are deferred until storage/tax phases.
