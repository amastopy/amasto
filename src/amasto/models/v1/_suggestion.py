from __future__ import annotations

from ._account import Account
from amasto._version import Unsupported, since
from pydantic import BaseModel, ConfigDict

__all__ = ("Suggestion",)


@since("3.4.0")
class Suggestion(BaseModel):
    model_config = ConfigDict(frozen=True)

    source: str | None = None
    sources: list[str] | Unsupported = since("4.3.0")
    account: Account
