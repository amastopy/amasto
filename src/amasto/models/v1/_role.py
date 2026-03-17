from __future__ import annotations

from amasto._version import since
from pydantic import BaseModel, ConfigDict

__all__ = ("Role",)


@since("4.0.0")
class Role(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    color: str
    permissions: str
    highlighted: bool
