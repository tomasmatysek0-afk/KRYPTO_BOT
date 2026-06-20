# codex_usage_budget

## Purpose

Track Plus-safe slice, checkpoint, and resume practices.

## Current conclusions

No important work may exist only in chat. `LOG.md`, `PROJECT_STATE.md`, and Git state must make the project restartable.

## Findings

### 2026-06-20 - Bootstrap
Source:
- CODEX_MASTER_PLAN.md

Summary:
Work must proceed in bounded slices with checkpoints and safe resume commands.

Decision impact:
Phase 00 creates `PROJECT_STATE.md` even though it is primarily a restartability artifact.

Open questions:
- None for Phase 00.
