from __future__ import annotations

from amasto._version import since
from pydantic import BaseModel, ConfigDict

__all__ = ("TermsOfService",)


@since("4.4.0")
class TermsOfService(BaseModel):
    model_config = ConfigDict(frozen=True)

    effective_date: str
    effective: bool
    content: str
    succeeded_by: str | None
