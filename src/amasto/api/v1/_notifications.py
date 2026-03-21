from __future__ import annotations

from ..._params import PaginationParams
from ..._resource import HttpMethod
from ...models.v1 import Notification, NotificationRequest
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("NotificationsResource",)


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


# ---------------------------------------------------------------------------
# Sub-resources
# ---------------------------------------------------------------------------


class _ClearResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, /) -> None:
        self.post: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "POST",
            "/api/v1/notifications/clear",
            dict,
        )


class _UnreadCountResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[dict, _UnreadCountParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/notifications/unread_count",
            dict,
            requires="4.3.0",
        )


class _RequestAcceptResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/notifications/requests/{id}/accept",
            dict,
            requires="4.3.0",
        )


class _RequestDismissResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/notifications/requests/{id}/dismiss",
            dict,
            requires="4.3.0",
        )


class _NotificationRequestByIdResource:
    __slots__ = ("accept", "dismiss")

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.accept = _RequestAcceptResource(client, id)
        self.dismiss = _RequestDismissResource(client, id)


class _BulkAcceptResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, /) -> None:
        self.post: HttpMethod[dict, None, _BulkRequestsBody] = HttpMethod(
            client,
            "POST",
            "/api/v1/notifications/requests/accept",
            dict,
            requires="4.3.0",
        )


class _BulkDismissResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, /) -> None:
        self.post: HttpMethod[dict, None, _BulkRequestsBody] = HttpMethod(
            client,
            "POST",
            "/api/v1/notifications/requests/dismiss",
            dict,
            requires="4.3.0",
        )


class _MergedResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/notifications/requests/merged",
            dict,
            requires="4.3.0",
        )


class _NotificationRequestsResource:
    __slots__ = ("_client", "accept", "dismiss", "get", "merged")

    def __init__(self, client: Amasto, /) -> None:
        self._client = client
        self.get: HttpMethod[list[NotificationRequest], PaginationParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/notifications/requests",
            list[NotificationRequest],
            requires="4.3.0",
        )
        self.accept = _BulkAcceptResource(client)
        self.dismiss = _BulkDismissResource(client)
        self.merged = _MergedResource(client)

    def __getitem__(self, id: str) -> _NotificationRequestByIdResource:
        return _NotificationRequestByIdResource(self._client, id)


class _NotificationDismissResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/notifications/{id}/dismiss",
            dict,
            requires="1.3.0",
        )


class _NotificationByIdResource:
    __slots__ = ("dismiss", "get")

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[Notification, None, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/notifications/{id}",
            Notification,
        )
        self.dismiss = _NotificationDismissResource(client, id)


# ---------------------------------------------------------------------------
# Top-level resource
# ---------------------------------------------------------------------------


class NotificationsResource:
    __slots__ = ("_client", "clear", "get", "requests", "unread_count")

    def __init__(self, client: Amasto, /) -> None:
        self._client = client
        self.get: HttpMethod[list[Notification], _NotificationsParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/notifications",
            list[Notification],
        )
        self.clear = _ClearResource(client)
        self.unread_count = _UnreadCountResource(client)
        self.requests = _NotificationRequestsResource(client)

    def __getitem__(self, id: str) -> _NotificationByIdResource:
        return _NotificationByIdResource(self._client, id)
