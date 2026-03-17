from __future__ import annotations

from amasto._version import Unsupported, since
from pydantic import BaseModel, ConfigDict

__all__ = ("Tag", "TagHistory")


@since("2.4.1")
class TagHistory(BaseModel):
    model_config = ConfigDict(frozen=True)

    day: str
    uses: str
    accounts: str


class Tag(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    url: str
    history: list[TagHistory] | Unsupported = since("2.4.1")
    following: bool | None | Unsupported = since("4.0.0")
    featuring: bool | None | Unsupported = since("4.4.0")
