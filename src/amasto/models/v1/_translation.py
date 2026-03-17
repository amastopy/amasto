from __future__ import annotations

from amasto._version import Unsupported, since
from pydantic import BaseModel, ConfigDict

__all__ = (
    "Translation",
    "TranslationAttachment",
    "TranslationPoll",
    "TranslationPollOption",
)


@since("4.2.0")
class TranslationPollOption(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str


@since("4.2.0")
class TranslationPoll(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    options: list[TranslationPollOption]


@since("4.2.0")
class TranslationAttachment(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    description: str


@since("4.0.0")
class Translation(BaseModel):
    model_config = ConfigDict(frozen=True)

    content: str
    detected_source_language: str
    provider: str
    language: str
    spoiler_text: str | Unsupported = since("4.2.0")
    poll: TranslationPoll | None | Unsupported = since("4.2.0")
    media_attachments: list[TranslationAttachment] | Unsupported = since("4.2.0")
