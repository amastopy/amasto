from __future__ import annotations

from ._account import Account
from ._application import Application
from ._custom_emoji import CustomEmoji
from ._media_attachment import MediaAttachment
from ._poll import Poll
from ._preview_card import PreviewCard
from ._quote import Quote, QuoteApproval, ShallowQuote
from amasto._version import Unsupported, since
from amasto.models.v2._filter import FilterResult
from pydantic import BaseModel, ConfigDict
from typing import Literal

__all__ = ("Status", "StatusMention", "StatusTag")


class StatusMention(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    username: str
    url: str
    acct: str


class StatusTag(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    url: str


class Status(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    uri: str
    created_at: str
    account: Account
    content: str
    reblogs_count: int
    favourites_count: int
    url: str | None
    in_reply_to_id: str | None
    in_reply_to_account_id: str | None
    reblog: Status | None
    media_attachments: list[MediaAttachment]
    mentions: list[StatusMention]
    tags: list[StatusTag]
    visibility: Literal["public", "unlisted", "private", "direct"]
    sensitive: bool
    application: Application | None
    spoiler_text: str | Unsupported = since("1.0.0")
    language: str | None | Unsupported = since("1.4.0")
    emojis: list[CustomEmoji] | Unsupported = since("2.0.0")
    replies_count: int | Unsupported = since("2.5.0")
    card: PreviewCard | None | Unsupported = since("2.6.0")
    poll: Poll | None | Unsupported = since("2.8.0")
    text: str | None | Unsupported = since("2.9.0")
    edited_at: str | None | Unsupported = since("3.5.0")
    quote: Quote | ShallowQuote | None | Unsupported = since("4.4.0")
    quotes_count: int | Unsupported = since("4.5.0")
    quote_approval: QuoteApproval | None | Unsupported = since("4.5.0")

    # Optional fields (only present with authorized user token)
    favourited: bool | None = None
    reblogged: bool | None = None
    muted: bool | None | Unsupported = since("1.4.0")
    bookmarked: bool | None | Unsupported = since("3.1.0")
    pinned: bool | None | Unsupported = since("1.6.0")
    filtered: list[FilterResult] | None | Unsupported = since("4.0.0")
