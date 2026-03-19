from __future__ import annotations

from ..._endpoint import Endpoint, SubscriptableEndpoint
from ..._params import PaginationParams
from ...models.v1 import Notification, NotificationRequest
from typing import TypedDict

__all__ = ("get_notifications", "notifications")


class _NotificationsParams(TypedDict, total=False):
    max_id: str
    since_id: str
    min_id: str
    limit: int
    types: list[str]
    exclude_types: list[str]
    account_id: str
    include_filtered: bool


class _UnreadCountParams(TypedDict, total=False):
    limit: int
    types: list[str]
    exclude_types: list[str]
    account_id: str


class _BulkRequestsBody(TypedDict):
    id: list[str]


get_notifications: SubscriptableEndpoint[list[Notification], _NotificationsParams, None, Notification] = (
    SubscriptableEndpoint(
        "GET",
        "/api/v1/notifications",
        list[Notification],
        "/api/v1/notifications/{id}",
        Notification,
        params=_NotificationsParams,
    )
)


class _NotificationRequestsById:
    __slots__ = ("post_accept", "post_dismiss")

    def __init__(self, id: str, /) -> None:
        self.post_accept = Endpoint("POST", f"/api/v1/notifications/requests/{id}/accept", dict, requires="4.3.0")
        self.post_dismiss = Endpoint("POST", f"/api/v1/notifications/requests/{id}/dismiss", dict, requires="4.3.0")


class _NotificationRequestsNamespace:
    __slots__ = ()

    post_accept: Endpoint[dict, None, _BulkRequestsBody] = Endpoint(
        "POST",
        "/api/v1/notifications/requests/accept",
        dict,
        body=_BulkRequestsBody,
        requires="4.3.0",
    )
    post_dismiss: Endpoint[dict, None, _BulkRequestsBody] = Endpoint(
        "POST",
        "/api/v1/notifications/requests/dismiss",
        dict,
        body=_BulkRequestsBody,
        requires="4.3.0",
    )
    get_merged: Endpoint[dict, None, None] = Endpoint(
        "GET",
        "/api/v1/notifications/requests/merged",
        dict,
        requires="4.3.0",
    )

    def __getitem__(self, id: str) -> _NotificationRequestsById:
        return _NotificationRequestsById(id)


class _NotificationsById:
    __slots__ = ("post_dismiss",)

    def __init__(self, id: str, /) -> None:
        self.post_dismiss = Endpoint("POST", f"/api/v1/notifications/{id}/dismiss", dict, requires="1.3.0")


class _NotificationsNamespace:
    __slots__ = ()

    post_clear = Endpoint("POST", "/api/v1/notifications/clear", dict)
    get_unread_count: Endpoint[dict, _UnreadCountParams, None] = Endpoint(
        "GET",
        "/api/v1/notifications/unread_count",
        dict,
        params=_UnreadCountParams,
        requires="4.3.0",
    )
    get_requests: Endpoint[list[NotificationRequest], PaginationParams, None] = Endpoint(
        "GET",
        "/api/v1/notifications/requests",
        list[NotificationRequest],
        params=PaginationParams,
        requires="4.3.0",
    )
    requests = _NotificationRequestsNamespace()

    def __getitem__(self, id: str) -> _NotificationsById:
        return _NotificationsById(id)


notifications = _NotificationsNamespace()
