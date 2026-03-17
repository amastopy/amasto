from __future__ import annotations

from ._account import Account
from ._status import Status
from ._tag import Tag
from amasto._version import since
from pydantic import BaseModel, ConfigDict

__all__ = ("Search",)


@since("1.1.0")
class Search(BaseModel):
    model_config = ConfigDict(frozen=True)

    accounts: list[Account]
    statuses: list[Status]
    hashtags: list[Tag]
