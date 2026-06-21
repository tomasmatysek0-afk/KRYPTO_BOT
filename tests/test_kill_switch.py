"""Tests for file and environment kill-switch behavior."""

from __future__ import annotations

from pathlib import Path

from coinbase_freqtrade_guarded_bot.guard_layer.kill_switch import is_kill_switch_active


class BrokenPath:
    """Path-like test double that raises during exists()."""

    def exists(self) -> bool:
        """Raise to exercise fail-closed filesystem uncertainty."""
        raise OSError("cannot inspect path")


def test_kill_switch_file_blocks_when_present(tmp_path: Path) -> None:
    """A present KILL_SWITCH file blocks intent evaluation."""
    kill_switch = tmp_path / "KILL_SWITCH"

    assert not is_kill_switch_active(path=kill_switch)
    kill_switch.write_text("halt\n", encoding="utf-8")
    assert is_kill_switch_active(path=kill_switch)


def test_kill_switch_env_halt_blocks(tmp_path: Path) -> None:
    """The CBOT_HALT environment flag blocks intents."""
    kill_switch = tmp_path / "missing"

    assert is_kill_switch_active(path=kill_switch, environment={"CBOT_HALT": "true"})
    assert is_kill_switch_active(path=kill_switch, environment={"CBOT_HALT": "1"})
    assert not is_kill_switch_active(path=kill_switch, environment={"CBOT_HALT": "false"})


def test_kill_switch_fails_closed_on_filesystem_error() -> None:
    """Filesystem uncertainty blocks intents."""
    assert is_kill_switch_active(path=BrokenPath())  # type: ignore[arg-type]
