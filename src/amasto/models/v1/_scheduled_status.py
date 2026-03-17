from __future__ import annotations

from ._media_attachment import MediaAttachment
from amasto._version import Unsupported, since
from pydantic import BaseModel, ConfigDict
from typing import Literal

__all__ = (
    "ScheduledStatus",
    "ScheduledStatusParams",
    "ScheduledStatusParamsPoll",
)


@since("2.8.0")
class ScheduledStatusParamsPoll(BaseModel):
    model_config = ConfigDict(frozen=True)

    options: list[str]
    expires_in: int
    multiple: bool | None = None
    hide_totals: bool | None = None


@since("2.7.0")
class ScheduledStatusParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str
    visibility: Literal["public", "unlisted", "private", "direct"]
    media_ids: list[str] | None = None
    sensitive: bool | None = None
    spoiler_text: str | None = None
    in_reply_to_id: int | None = None
    language: str | None = None
    scheduled_at: None = None
    idempotency: str | None = None
    poll: ScheduledStatusParamsPoll | None | Unsupported = since("2.8.0")


@since("2.7.0")
class ScheduledStatus(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    scheduled_at: str
    params: ScheduledStatusParams
    media_attachments: list[MediaAttachment]
