from __future__ import annotations

from amasto._version import since
from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from amasto.models.v1._status import Status

__all__ = ("Quote", "QuoteApproval", "ShallowQuote")

_QUOTE_STATE = Literal[
    "pending",
    "accepted",
    "rejected",
    "revoked",
    "deleted",
    "unauthorized",
    "blocked_account",
    "blocked_domain",
    "muted_account",
]


@since("4.5.0")
class QuoteApproval(BaseModel):
    model_config = ConfigDict(frozen=True)

    automatic: list[str]
    manual: list[str]
    current_user: Literal["automatic", "manual", "denied", "unknown"]


@since("4.4.0")
class ShallowQuote(BaseModel):
    model_config = ConfigDict(frozen=True)

    state: _QUOTE_STATE
    quoted_status_id: str | None


@since("4.4.0")
class Quote(BaseModel):
    model_config = ConfigDict(frozen=True)

    state: _QUOTE_STATE
    quoted_status: Status | None = None
