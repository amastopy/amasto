from __future__ import annotations

from amasto._version import since
from pydantic import BaseModel, ConfigDict

__all__ = ("StatusSource",)


@since("3.5.0")
class StatusSource(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    text: str
    spoiler_text: str
