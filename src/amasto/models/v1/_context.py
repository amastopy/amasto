from __future__ import annotations

from ._status import Status
from amasto._version import since
from pydantic import BaseModel, ConfigDict

__all__ = ("Context",)


@since("0.6.0")
class Context(BaseModel):
    model_config = ConfigDict(frozen=True)

    ancestors: list[Status]
    descendants: list[Status]
