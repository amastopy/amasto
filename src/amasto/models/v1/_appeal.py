from __future__ import annotations

from amasto._version import since
from pydantic import BaseModel, ConfigDict
from typing import Literal

__all__ = ("Appeal",)


@since("4.3.0")
class Appeal(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str
    state: Literal["approved", "rejected", "pending"]
