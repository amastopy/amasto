from __future__ import annotations

from amasto._version import since
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

__all__ = ("Preferences",)


@since("2.8.0")
class Preferences(BaseModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    posting_default_visibility: Literal["public", "unlisted", "private", "direct"] = Field(
        alias="posting:default:visibility"
    )
    posting_default_sensitive: bool = Field(alias="posting:default:sensitive")
    posting_default_language: str | None = Field(default=None, alias="posting:default:language")
    reading_expand_media: Literal["default", "show_all", "hide_all"] = Field(alias="reading:expand:media")
    reading_expand_spoilers: bool = Field(alias="reading:expand:spoilers")
