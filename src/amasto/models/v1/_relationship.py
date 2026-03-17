from __future__ import annotations

from amasto._version import Unsupported, since
from pydantic import BaseModel, ConfigDict

__all__ = ("Relationship",)


class Relationship(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    following: bool
    showing_reblogs: bool | Unsupported = since("2.1.0")
    notifying: bool | Unsupported = since("3.3.0")
    languages: list[str] | None | Unsupported = since("4.0.0")
    followed_by: bool
    blocking: bool
    blocked_by: bool | Unsupported = since("2.8.0")
    muting: bool | Unsupported = since("1.1.0")
    muting_notifications: bool | Unsupported = since("2.1.0")
    requested: bool | Unsupported = since("0.9.9")
    requested_by: bool | Unsupported = since("4.1.0")
    domain_blocking: bool | Unsupported = since("1.4.0")
    endorsed: bool | Unsupported = since("2.5.0")
    note: str | Unsupported = since("3.2.0")
