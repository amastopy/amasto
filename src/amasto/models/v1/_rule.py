from __future__ import annotations

from amasto._version import Unsupported, since
from pydantic import BaseModel, ConfigDict

__all__ = ("Rule",)


@since("3.4.0")
class Rule(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    text: str
    hint: str | Unsupported = since("4.3.0")
    translations: dict[str, dict[str, str]] | Unsupported = since("4.4.0")
