"""File and environment based kill-switch checks."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

DEFAULT_KILL_SWITCH_PATH = Path("KILL_SWITCH")
HALT_ENV_VAR = "CBOT_HALT"
TRUE_VALUES = {"1", "true", "yes", "on"}


def is_kill_switch_active(
    *,
    path: Path = DEFAULT_KILL_SWITCH_PATH,
    environment: Mapping[str, str] | None = None,
) -> bool:
    """Return true when file or environment halt conditions are active.

    The check fails closed: filesystem uncertainty returns active.
    """
    env = environment or {}
    if env.get(HALT_ENV_VAR, "").strip().lower() in TRUE_VALUES:
        return True
    try:
        return path.exists()
    except OSError:
        return True
