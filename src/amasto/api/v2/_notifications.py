from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import Account
from ...models.v2 import NotificationPolicy
from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("NotificationsResource",)


# ---------------------------------------------------------------------------
# TypedDicts
# ---------------------------------------------------------------------------


class _GroupedNotificationsParams(TypedDict, total=False):
    max_id: str
    since_id: str
    min_id: str
    limit: int
    types: list[str | Literal["mention", "status", "reblog", "follow", "follow_request", "favourite", "poll", "update", "admin.sign_up", "admin.report"]]
    exclude_types: list[str | Literal["mention", "status", "reblog", "follow", "follow_request", "favourite", "poll", "update", "admin.sign_up", "admin.report"]]
    account_id: str
    expand_accounts: str | Literal["full", "partial_avatars"]
    grouped_types: list[str | Literal["mention", "status", "reblog", "follow", "follow_request", "favourite", "poll", "update", "admin.sign_up", "admin.report"]]
    include_filtered: bool


class _UnreadCountParams(TypedDict, total=False):
    limit: int
    types: list[str | Literal["mention", "status", "reblog", "follow", "follow_request", "favourite", "poll", "update", "admin.sign_up", "admin.report"]]
    exclude_types: list[str | Literal["mention", "status", "reblog", "follow", "follow_request", "favourite", "poll", "update", "admin.sign_up", "admin.report"]]
    account_id: str
    grouped_types: list[str | Literal["mention", "status", "reblog", "follow", "follow_request", "favourite", "poll", "update", "admin.sign_up", "admin.report"]]


class _UpdatePolicyBody(TypedDict, total=False):
    for_not_following: str | Literal["accept", "filter", "drop"]
    for_not_followers: str | Literal["accept", "filter", "drop"]
    for_new_accounts: str | Literal["accept", "filter", "drop"]
    for_private_mentions: str | Literal["accept", "filter", "drop"]
    for_limited_accounts: str | Literal["accept", "filter", "drop"]


# ---------------------------------------------------------------------------
# Sub-resources
# ---------------------------------------------------------------------------


class _UnreadCountResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[dict, _UnreadCountParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v2/notifications/unread_count",
            dict,
            requires="4.3.0",
        )


class _PolicyResource:
    __slots__ = ("get", "patch")

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[NotificationPolicy, None, None] = HttpMethod(
            client,
            "GET",
            "/api/v2/notifications/policy",
            NotificationPolicy,
            requires="4.3.0",
        )
        self.patch: HttpMethod[NotificationPolicy, None, _UpdatePolicyBody] = HttpMethod(
            client,
            "PATCH",
            "/api/v2/notifications/policy",
            NotificationPolicy,
            requires="4.3.0",
        )


class _DismissResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, group_key: str, /) -> None:
        self.post: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v2/notifications/{group_key}/dismiss",
            dict,
            requires="4.3.0",
        )


class _AccountsResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, group_key: str, /) -> None:
        self.get: HttpMethod[list[Account], None, None] = HttpMethod(
            client,
            "GET",
            f"/api/v2/notifications/{group_key}/accounts",
            list[Account],
            requires="4.3.0",
        )


class _NotificationByGroupKeyResource:
    __slots__ = ("accounts", "dismiss")

    def __init__(self, client: Amasto, group_key: str, /) -> None:
        self.dismiss = _DismissResource(client, group_key)
        self.accounts = _AccountsResource(client, group_key)


# ---------------------------------------------------------------------------
# Top-level resource
# ---------------------------------------------------------------------------


class NotificationsResource:
    __slots__ = ("_client", "get", "policy", "unread_count")

    def __init__(self, client: Amasto, /) -> None:
        self._client = client
        self.get: HttpMethod[dict, _GroupedNotificationsParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v2/notifications",
            dict,
            requires="4.3.0",
        )
        self.unread_count = _UnreadCountResource(client)
        self.policy = _PolicyResource(client)

    def __getitem__(self, group_key: str) -> _NotificationByGroupKeyResource:
        return _NotificationByGroupKeyResource(self._client, group_key)
