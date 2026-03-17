from __future__ import annotations

from ._account import Account
from ._custom_emoji import CustomEmoji
from ._media_attachment import MediaAttachment
from ._quote import Quote, ShallowQuote
from amasto._version import Unsupported, since
from pydantic import BaseModel, ConfigDict

__all__ = ("StatusEdit", "StatusEditPoll", "StatusEditPollOption")


@since("3.5.0")
class StatusEditPollOption(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str


@since("3.5.0")
class StatusEditPoll(BaseModel):
    model_config = ConfigDict(frozen=True)

    options: list[StatusEditPollOption]


@since("3.5.0")
class StatusEdit(BaseModel):
    model_config = ConfigDict(frozen=True)

    content: str
    spoiler_text: str
    sensitive: bool
    created_at: str
    account: Account
    poll: StatusEditPoll | None = None
    media_attachments: list[MediaAttachment]
    emojis: list[CustomEmoji]
    quote: Quote | ShallowQuote | None | Unsupported = since("4.4.0")
