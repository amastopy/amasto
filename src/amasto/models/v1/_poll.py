from __future__ import annotations

from ._custom_emoji import CustomEmoji
from amasto._version import since
from pydantic import BaseModel, ConfigDict

__all__ = ("Poll", "PollOption")


@since("2.8.0")
class PollOption(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    votes_count: int | None


@since("2.8.0")
class Poll(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    expires_at: str | None
    expired: bool
    multiple: bool
    votes_count: int
    voters_count: int | None
    options: list[PollOption]
    emojis: list[CustomEmoji]
    voted: bool | None = None
    own_votes: list[int] | None = None
