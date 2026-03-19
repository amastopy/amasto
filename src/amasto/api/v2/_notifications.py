from __future__ import annotations

from ..._endpoint import Endpoint
from ...models.v1 import Account
from typing import TypedDict

__all__ = ("get_notifications", "notifications")


# ---------------------------------------------------------------------------
# TypedDicts
# ---------------------------------------------------------------------------


class _GroupedNotificationsParams(TypedDict, total=False):
    max_id: str
    since_id: str
    min_id: str
    limit: int
    types: list[str]
    exclude_types: list[str]
    account_id: str
    expand_accounts: str
    grouped_types: list[str]
    include_filtered: bool


class _UnreadCountParams(TypedDict, total=False):
    limit: int
    types: list[str]
    exclude_types: list[str]
    account_id: str
    grouped_types: list[str]


# ---------------------------------------------------------------------------
# Flat endpoints
# ---------------------------------------------------------------------------


get_notifications: Endpoint[dict, _GroupedNotificationsParams, None] = Endpoint(
    "GET",
    "/api/v2/notifications",
    dict,
    params=_GroupedNotificationsParams,
    requires="4.3.0",
)


# ---------------------------------------------------------------------------
# By-group-key namespace
# ---------------------------------------------------------------------------


class _NotificationsByGroupKey:
    __slots__ = ("get_accounts", "post_dismiss")

    def __init__(self, group_key: str, /) -> None:
        p = f"/api/v2/notifications/{group_key}"
        self.post_dismiss = Endpoint("POST", f"{p}/dismiss", dict, requires="4.3.0")
        self.get_accounts: Endpoint[list[Account], None, None] = Endpoint(
            "GET",
            f"{p}/accounts",
            list[Account],
            requires="4.3.0",
        )


class _NotificationsNamespace:
    __slots__ = ()

    get_unread_count: Endpoint[dict, _UnreadCountParams, None] = Endpoint(
        "GET",
        "/api/v2/notifications/unread_count",
        dict,
        params=_UnreadCountParams,
        requires="4.3.0",
    )

    def __getitem__(self, group_key: str) -> _NotificationsByGroupKey:
        return _NotificationsByGroupKey(group_key)


notifications = _NotificationsNamespace()
