from __future__ import annotations

from ._account import Account
from ._tag import TagHistory
from amasto._version import Unsupported, since
from pydantic import BaseModel, ConfigDict
from typing import Literal

__all__ = ("PreviewCard", "PreviewCardAuthor", "TrendsLink")


@since("4.3.0")
class PreviewCardAuthor(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    url: str
    account: Account | None = None


class PreviewCard(BaseModel):
    model_config = ConfigDict(frozen=True)

    url: str
    title: str
    description: str
    type: Literal["link", "photo", "video", "rich"] | Unsupported = since("1.3.0")
    authors: list[PreviewCardAuthor] | Unsupported = since("4.3.0")
    author_name: str | Unsupported = since("1.3.0")
    author_url: str | Unsupported = since("1.3.0")
    provider_name: str | Unsupported = since("1.3.0")
    provider_url: str | Unsupported = since("1.3.0")
    html: str | Unsupported = since("1.3.0")
    width: int | Unsupported = since("1.3.0")
    height: int | Unsupported = since("1.3.0")
    image: str | None = None
    embed_url: str | Unsupported = since("2.1.0")
    blurhash: str | None | Unsupported = since("3.2.0")


class TrendsLink(PreviewCard):
    history: list[TagHistory] | Unsupported = since("3.5.0")
