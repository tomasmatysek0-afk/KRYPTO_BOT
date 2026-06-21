# Kill Switch

## Purpose

The kill-switch is a fail-closed local guard. If it is active, order intents are rejected and must still be audited.

## Local Mechanisms

- File: `KILL_SWITCH` in the repository working directory.
- Environment flag: `CBOT_HALT=true`, `CBOT_HALT=1`, `CBOT_HALT=yes`, or `CBOT_HALT=on`.

If the kill-switch file exists, the minimal guard core treats the system as halted.

If the kill-switch state cannot be read safely, the guard must fail closed.

## Safety Rules

- The kill-switch does not enable live trading.
- The kill-switch is not a UI-only toggle.
- Rejected intents caused by the kill-switch are written to audit JSONL.
- Removing the file only removes this local halt condition; all other risk checks still apply.

## Current Status

Implemented in Phase 05b:

- `src/coinbase_freqtrade_guarded_bot/guard_layer/kill_switch.py`
- `tests/test_kill_switch.py`

Runtime exchange reconciliation and full Phase 09 guard behavior remain future work.
