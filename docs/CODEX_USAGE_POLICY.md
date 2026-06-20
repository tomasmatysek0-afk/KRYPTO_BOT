# Codex Usage Policy

## Plus-Safe Slices

Work proceeds in bounded slices:

- a small phase;
- a subphase;
- or one clear acceptance block.

Each slice must update `LOG.md`, update `PROJECT_STATE.md`, run relevant checks, propose or create a commit, and push when passing.

## Persistence

No important work may exist only in chat. Restartability requires:

- project files on disk;
- `LOG.md`;
- `PROJECT_STATE.md`;
- known Git status;
- latest safe next command;
- ideally a pushed commit.

## Quota-Safe Checkpoint

Before long tests, backtests, refactors, or ending a response, write a `QUOTA_SAFE_CHECKPOINT` with:

- current slice;
- changed files;
- tests run;
- Git status;
- recommended commit message;
- next deterministic command;
- resume instructions.

## Hard Stop

If a usage limit warning appears, stop expanding scope, finish or safely discard the current small step, update state files, and provide resume instructions.
