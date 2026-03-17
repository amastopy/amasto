from __future__ import annotations

from ._account import Account
from ._rule import Rule
from amasto._version import Unsupported, since
from pydantic import BaseModel, ConfigDict

__all__ = (
    "Instance",
    "InstanceConfiguration",
    "InstanceConfigurationAccounts",
    "InstanceConfigurationMediaAttachments",
    "InstanceConfigurationPolls",
    "InstanceConfigurationStatuses",
    "InstanceStats",
    "InstanceUrls",
)


@since("1.4.2")
class InstanceUrls(BaseModel):
    model_config = ConfigDict(frozen=True)

    streaming_api: str


@since("1.6.0")
class InstanceStats(BaseModel):
    model_config = ConfigDict(frozen=True)

    user_count: int
    status_count: int
    domain_count: int


@since("4.0.0")
class InstanceConfigurationAccounts(BaseModel):
    model_config = ConfigDict(frozen=True)

    max_featured_tags: int


@since("3.4.2")
class InstanceConfigurationStatuses(BaseModel):
    model_config = ConfigDict(frozen=True)

    max_characters: int
    max_media_attachments: int
    characters_reserved_per_url: int


@since("3.4.2")
class InstanceConfigurationMediaAttachments(BaseModel):
    model_config = ConfigDict(frozen=True)

    supported_mime_types: list[str]
    image_size_limit: int
    image_matrix_limit: int
    video_size_limit: int
    video_frame_rate_limit: int
    video_matrix_limit: int


@since("3.4.2")
class InstanceConfigurationPolls(BaseModel):
    model_config = ConfigDict(frozen=True)

    max_options: int
    max_characters_per_option: int
    min_expiration: int
    max_expiration: int


@since("3.4.2")
class InstanceConfiguration(BaseModel):
    model_config = ConfigDict(frozen=True)

    statuses: InstanceConfigurationStatuses
    media_attachments: InstanceConfigurationMediaAttachments
    polls: InstanceConfigurationPolls
    accounts: InstanceConfigurationAccounts | Unsupported = since("4.0.0")


@since("1.1.0")
class Instance(BaseModel):
    model_config = ConfigDict(frozen=True)

    uri: str
    title: str
    description: str
    email: str
    version: str | Unsupported = since("1.3.0")
    urls: InstanceUrls | Unsupported = since("1.4.2")
    stats: InstanceStats | Unsupported = since("1.6.0")
    thumbnail: str | None | Unsupported = since("1.6.1")
    languages: list[str] | Unsupported = since("2.3.0")
    contact_account: Account | None | Unsupported = since("2.3.0")
    registrations: bool | Unsupported = since("2.7.2")
    short_description: str | Unsupported = since("2.9.2")
    approval_required: bool | Unsupported = since("2.9.2")
    invites_enabled: bool | Unsupported = since("3.1.4")
    rules: list[Rule] | Unsupported = since("3.4.0")
    configuration: InstanceConfiguration | Unsupported = since("3.4.2")
