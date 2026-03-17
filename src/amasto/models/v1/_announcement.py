from __future__ import annotations

from ._custom_emoji import CustomEmoji
from ._reaction import Reaction
from ._status import StatusTag
from amasto._version import since
from pydantic import BaseModel, ConfigDict

__all__ = ("Announcement", "AnnouncementAccount", "AnnouncementStatus")


@since("3.1.0")
class AnnouncementAccount(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    username: str
    url: str
    acct: str


@since("3.1.0")
class AnnouncementStatus(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    url: str


@since("3.1.0")
class Announcement(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    content: str
    starts_at: str | None
    ends_at: str | None
    all_day: bool
    published_at: str
    updated_at: str
    read: bool | None = None
    mentions: list[AnnouncementAccount]
    statuses: list[AnnouncementStatus]
    tags: list[StatusTag]
    emojis: list[CustomEmoji]
    reactions: list[Reaction]
