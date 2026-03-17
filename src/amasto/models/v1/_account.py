from __future__ import annotations

from ._custom_emoji import CustomEmoji
from ._role import Role
from amasto._version import Unsupported, since
from pydantic import BaseModel, ConfigDict
from typing import Literal

__all__ = (
    "Account",
    "AccountRole",
    "AccountSource",
    "CredentialAccount",
    "Field",
    "MutedAccount",
)


@since("2.4.0")
class Field(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    value: str
    verified_at: str | None | Unsupported = since("2.6.0")


@since("4.1.0")
class AccountRole(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    color: str


@since("1.5.0")
class AccountSource(BaseModel):
    model_config = ConfigDict(frozen=True)

    note: str
    privacy: Literal["public", "unlisted", "private", "direct"]
    sensitive: bool
    fields: list[Field] | Unsupported = since("2.4.0")
    language: str | Unsupported = since("2.4.2")
    follow_requests_count: int | Unsupported = since("3.0.0")
    discoverable: bool | None | Unsupported = since("3.1.0")
    hide_collections: bool | None | Unsupported = since("4.1.0")
    indexable: bool | Unsupported = since("4.3.0")
    attribution_domains: list[str] | Unsupported = since("4.4.0")
    quote_policy: Literal["public", "followers", "nobody"] | Unsupported = since("4.5.0")


class Account(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    username: str
    acct: str
    url: str | None
    display_name: str
    note: str
    avatar: str
    header: str
    locked: bool
    created_at: str
    statuses_count: int
    followers_count: int
    following_count: int

    avatar_static: str | Unsupported = since("1.1.2")
    header_static: str | Unsupported = since("1.1.2")
    moved: Account | None | Unsupported = since("2.1.0")
    fields: list[Field] | Unsupported = since("2.4.0")
    emojis: list[CustomEmoji] | Unsupported = since("2.4.0")
    bot: bool | Unsupported = since("2.4.0")
    last_status_at: str | None | Unsupported = since("3.0.0")
    group: bool | Unsupported = since("3.1.0")
    discoverable: bool | None | Unsupported = since("3.1.0")
    suspended: bool | None | Unsupported = since("3.3.0")
    limited: bool | None | Unsupported = since("3.5.3")
    noindex: bool | None | Unsupported = since("4.0.0")
    roles: list[AccountRole] | None | Unsupported = since("4.1.0")
    uri: str | Unsupported = since("4.2.0")
    memorial: bool | None | Unsupported = since("4.2.0")
    indexable: bool | Unsupported = since("4.3.0")
    hide_collections: bool | None | Unsupported = since("4.3.0")


class CredentialAccount(Account):
    source: AccountSource | Unsupported = since("1.5.0")
    role: Role | Unsupported = since("4.0.0")


@since("3.3.0")
class MutedAccount(Account):
    mute_expires_at: str | None
