from __future__ import annotations

from amasto._version import since
from pydantic import BaseModel, ConfigDict
from typing import Literal

__all__ = ("Filter", "FilterKeyword", "FilterResult", "FilterStatus")


@since("4.0.0")
class FilterKeyword(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    keyword: str
    whole_word: bool


@since("4.0.0")
class FilterStatus(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    status_id: str


@since("4.0.0")
class Filter(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    title: str
    context: list[Literal["home", "notifications", "public", "thread", "account"]]
    expires_at: str | None
    filter_action: Literal["warn", "hide", "blur"]
    keywords: list[FilterKeyword] | None = None
    statuses: list[FilterStatus] | None = None


@since("4.0.0")
class FilterResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    filter: Filter
    keyword_matches: list[str] | None
    status_matches: list[str] | None
