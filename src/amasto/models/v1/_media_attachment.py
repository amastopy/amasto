from __future__ import annotations

from amasto._version import Unsupported, since
from pydantic import BaseModel, ConfigDict
from typing import Any, Literal

__all__ = ("MediaAttachment",)


class MediaAttachment(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    type: Literal["unknown", "image", "gifv", "video", "audio"]
    url: str | None
    preview_url: str | None
    remote_url: str | None = None
    meta: dict[str, Any] | None | Unsupported = since("1.5.0")
    description: str | None | Unsupported = since("2.0.0")
    blurhash: str | None | Unsupported = since("2.8.1")
