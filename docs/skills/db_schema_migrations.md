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

### 2026-06-20 - Phase 00b schema policy document
Source:
- CODEX_MASTER_PLAN.md
- docs/DB_SCHEMA_POLICY.md

Summary:
Runtime databases remain ignored. Schema versioning and migration tests are required once SQLite storage is introduced.

Decision impact:
No DB dependency or ORM is added in Phase 00b.

Open questions:
- None.
