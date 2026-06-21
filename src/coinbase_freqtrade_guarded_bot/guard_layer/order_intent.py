"""Typed order intent and risk decision domain models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from typing import Literal, TypeAlias

OrderSide: TypeAlias = Literal["buy", "sell"]
PositionEffect: TypeAlias = Literal["open", "close"]
OrderType: TypeAlias = Literal["limit", "market"]
TradingMode: TypeAlias = Literal["spot"]

SUPPORTED_PAIRS = {"BTC/USD", "ETH/USD"}
SUPPORTED_QUOTE = "USD"


class GuardModelError(ValueError):
    """Raised when a guard domain model is invalid."""


@dataclass(frozen=True, slots=True)
class OrderIntent:
    """Proposed order intent before any execution or preview path."""

    intent_id: str
    pair: str
    side: OrderSide
    position_effect: PositionEffect
    stake_amount: Decimal
    quote_currency: str = SUPPORTED_QUOTE
    order_type: OrderType = "limit"
    dry_run: bool = True
    trading_mode: TradingMode = "spot"
    leverage: Decimal = Decimal("1")
    strategy_name: str = "CoinbaseTrendGuardV1"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.intent_id:
            raise GuardModelError("intent_id is required.")
        if self.pair not in SUPPORTED_PAIRS:
            raise GuardModelError(f"Unsupported pair: {self.pair}")
        if self.quote_currency != SUPPORTED_QUOTE:
            raise GuardModelError(f"Unsupported quote currency: {self.quote_currency}")
        if self.stake_amount <= 0:
            raise GuardModelError("stake_amount must be positive.")
        if self.leverage <= 0:
            raise GuardModelError("leverage must be positive.")
        if self.created_at.tzinfo is None:
            raise GuardModelError("created_at must be timezone-aware.")
        object.__setattr__(self, "created_at", self.created_at.astimezone(UTC))

    def to_audit_dict(self) -> dict[str, object]:
        """Serialize the intent into JSON-compatible audit data."""
        data = asdict(self)
        data["stake_amount"] = str(self.stake_amount)
        data["leverage"] = str(self.leverage)
        data["created_at"] = self.created_at.isoformat()
        return data


@dataclass(frozen=True, slots=True)
class RiskDecision:
    """Risk decision for an order intent."""

    intent_id: str
    approved: bool
    reason_code: str
    reason: str
    checked_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.intent_id:
            raise GuardModelError("intent_id is required.")
        if not self.reason_code:
            raise GuardModelError("reason_code is required.")
        if self.checked_at.tzinfo is None:
            raise GuardModelError("checked_at must be timezone-aware.")
        object.__setattr__(self, "checked_at", self.checked_at.astimezone(UTC))

    @classmethod
    def approve(
        cls,
        intent: OrderIntent,
        reason: str = "Intent passed minimal guards.",
    ) -> RiskDecision:
        """Create an approval decision for an intent."""
        return cls(
            intent_id=intent.intent_id,
            approved=True,
            reason_code="approved",
            reason=reason,
        )

    @classmethod
    def reject(cls, intent: OrderIntent, reason_code: str, reason: str) -> RiskDecision:
        """Create a rejection decision for an intent."""
        return cls(
            intent_id=intent.intent_id,
            approved=False,
            reason_code=reason_code,
            reason=reason,
        )

    def to_audit_dict(self) -> dict[str, object]:
        """Serialize the decision into JSON-compatible audit data."""
        data = asdict(self)
        data["checked_at"] = self.checked_at.isoformat()
        return data
