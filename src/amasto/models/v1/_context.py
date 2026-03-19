from __future__ import annotations

from ._status import Status
from pydantic import BaseModel, ConfigDict

__all__ = ("Context",)


class Context(BaseModel):
    model_config = ConfigDict(frozen=True)

    ancestors: list[Status]
    descendants: list[Status]
