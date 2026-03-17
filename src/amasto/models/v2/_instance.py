from __future__ import annotations

from amasto._version import Unsupported, since
from amasto.models.v1._account import Account
from amasto.models.v1._rule import Rule
from pydantic import BaseModel, ConfigDict, Field

__all__ = (
    "Instance",
    "InstanceConfiguration",
    "InstanceConfigurationAccounts",
    "InstanceConfigurationMediaAttachments",
    "InstanceConfigurationPolls",
    "InstanceConfigurationStatuses",
    "InstanceConfigurationTimelinesAccess",
    "InstanceConfigurationTimelinesFeedAccess",
    "InstanceConfigurationTranslation",
    "InstanceConfigurationUrls",
    "InstanceConfigurationVapid",
    "InstanceContact",
    "InstanceIcon",
    "InstanceRegistrations",
    "InstanceThumbnail",
    "InstanceThumbnailVersions",
    "InstanceUsage",
    "InstanceUsageUsers",
)


@since("4.0.0")
class InstanceUsageUsers(BaseModel):
    model_config = ConfigDict(frozen=True)

    active_month: int


@since("4.0.0")
class InstanceUsage(BaseModel):
    model_config = ConfigDict(frozen=True)

    users: InstanceUsageUsers


@since("4.0.0")
class InstanceThumbnailVersions(BaseModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    one_x: str | None = Field(default=None, alias="@1x")
    two_x: str | None = Field(default=None, alias="@2x")


@since("4.0.0")
class InstanceThumbnail(BaseModel):
    model_config = ConfigDict(frozen=True)

    url: str
    blurhash: str | None = None
    versions: InstanceThumbnailVersions | None = None


@since("4.3.0")
class InstanceIcon(BaseModel):
    model_config = ConfigDict(frozen=True)

    src: str
    size: str


@since("4.0.0")
class InstanceConfigurationUrls(BaseModel):
    model_config = ConfigDict(frozen=True)

    streaming: str
    status: str | None | Unsupported = since("4.1.0")
    about: str | Unsupported = since("4.4.0")
    privacy_policy: str | None | Unsupported = since("4.4.0")
    terms_of_service: str | None | Unsupported = since("4.4.0")


@since("4.3.0")
class InstanceConfigurationVapid(BaseModel):
    model_config = ConfigDict(frozen=True)

    public_key: str


@since("4.0.0")
class InstanceConfigurationAccounts(BaseModel):
    model_config = ConfigDict(frozen=True)

    max_featured_tags: int
    max_pinned_statuses: int | Unsupported = since("4.3.0")
    max_profile_fields: int | Unsupported = since("4.6.0")
    profile_field_name_limit: int | Unsupported = since("4.6.0")
    profile_field_value_limit: int | Unsupported = since("4.6.0")


@since("4.0.0")
class InstanceConfigurationStatuses(BaseModel):
    model_config = ConfigDict(frozen=True)

    max_characters: int
    max_media_attachments: int
    characters_reserved_per_url: int


@since("4.0.0")
class InstanceConfigurationMediaAttachments(BaseModel):
    model_config = ConfigDict(frozen=True)

    supported_mime_types: list[str]
    image_size_limit: int
    image_matrix_limit: int
    video_size_limit: int
    video_frame_rate_limit: int
    video_matrix_limit: int
    description_limit: int | Unsupported = since("4.4.0")


@since("4.0.0")
class InstanceConfigurationPolls(BaseModel):
    model_config = ConfigDict(frozen=True)

    max_options: int
    max_characters_per_option: int
    min_expiration: int
    max_expiration: int


@since("4.0.0")
class InstanceConfigurationTranslation(BaseModel):
    model_config = ConfigDict(frozen=True)

    enabled: bool


@since("4.5.0")
class InstanceConfigurationTimelinesFeedAccess(BaseModel):
    model_config = ConfigDict(frozen=True)

    local: str
    remote: str


@since("4.5.0")
class InstanceConfigurationTimelinesAccess(BaseModel):
    model_config = ConfigDict(frozen=True)

    live_feeds: InstanceConfigurationTimelinesFeedAccess
    hashtag_feeds: InstanceConfigurationTimelinesFeedAccess
    trending_link_feeds: InstanceConfigurationTimelinesFeedAccess


@since("4.0.0")
class InstanceConfiguration(BaseModel):
    model_config = ConfigDict(frozen=True)

    urls: InstanceConfigurationUrls
    accounts: InstanceConfigurationAccounts
    statuses: InstanceConfigurationStatuses
    media_attachments: InstanceConfigurationMediaAttachments
    polls: InstanceConfigurationPolls
    translation: InstanceConfigurationTranslation
    vapid: InstanceConfigurationVapid | Unsupported = since("4.3.0")
    timelines_access: InstanceConfigurationTimelinesAccess | Unsupported = since("4.5.0")
    limited_federation: bool | Unsupported = since("4.4.0")


@since("4.0.0")
class InstanceRegistrations(BaseModel):
    model_config = ConfigDict(frozen=True)

    enabled: bool
    approval_required: bool
    message: str | None
    url: str | None | Unsupported = since("4.2.0")
    reason_required: bool | None | Unsupported = since("4.4.0")
    min_age: int | None | Unsupported = since("4.4.0")


@since("4.0.0")
class InstanceContact(BaseModel):
    model_config = ConfigDict(frozen=True)

    email: str
    account: Account | None


@since("4.0.0")
class Instance(BaseModel):
    model_config = ConfigDict(frozen=True)

    domain: str
    title: str
    version: str
    source_url: str
    description: str
    usage: InstanceUsage
    thumbnail: InstanceThumbnail
    languages: list[str]
    configuration: InstanceConfiguration
    registrations: InstanceRegistrations
    contact: InstanceContact
    rules: list[Rule]
    icon: list[InstanceIcon] | Unsupported = since("4.3.0")
    api_versions: dict[str, int] | Unsupported = since("4.3.0")
