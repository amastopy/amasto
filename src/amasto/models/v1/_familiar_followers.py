from __future__ import annotations

from ._account import Account
from amasto._version import since
from pydantic import BaseModel, ConfigDict

__all__ = ("FamiliarFollowers",)


@since("3.5.0")
class FamiliarFollowers(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    accounts: list[Account]
