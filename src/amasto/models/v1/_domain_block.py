from __future__ import annotations

from amasto._version import since
from pydantic import BaseModel, ConfigDict
from typing import Literal

__all__ = ("DomainBlock",)


@since("4.0.0")
class DomainBlock(BaseModel):
    model_config = ConfigDict(frozen=True)

    domain: str
    digest: str
    severity: Literal["silence", "suspend"]
    comment: str | None = None
