# db_schema_migrations

## Purpose

Track local DB schema versioning, migration, backup, and reset policy.

## Current conclusions

DB work is deferred. Runtime databases must not be committed.

## Findings

### 2026-06-20 - Bootstrap
Source:
- CODEX_MASTER_PLAN.md

Summary:
SQLite schema versioning and migration policy become relevant in later storage and tax phases.

Decision impact:
`.gitignore` excludes local database files.

Open questions:
- None for Phase 00.
