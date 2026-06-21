"""Append-only JSONL audit writer for guard decisions."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from coinbase_freqtrade_guarded_bot.guard_layer.order_intent import OrderIntent, RiskDecision


class AuditWriteError(OSError):
    """Raised when an audit record cannot be written."""


@dataclass(frozen=True, slots=True)
class AuditWriter:
    """Append-only JSONL audit writer."""

    path: Path

    def write_decision(self, intent: OrderIntent, decision: RiskDecision) -> None:
        """Append a guard decision record to JSONL audit storage."""
        record = {
            "record_type": "guard_decision",
            "written_at": datetime.now(UTC).isoformat(),
            "intent": intent.to_audit_dict(),
            "decision": decision.to_audit_dict(),
        }
        self._append_record(record)

    def _append_record(self, record: dict[str, object]) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as audit_file:
                audit_file.write(json.dumps(record, sort_keys=True, separators=(",", ":")))
                audit_file.write("\n")
        except OSError as exc:
            raise AuditWriteError(f"Failed to write audit record to {self.path}") from exc
