from __future__ import annotations

from amasto._version import since
from pydantic import BaseModel, ConfigDict

__all__ = ("ExtendedDescription",)


@since("4.0.0")
class ExtendedDescription(BaseModel):
    model_config = ConfigDict(frozen=True)

    updated_at: str
    content: str
