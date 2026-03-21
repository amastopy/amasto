from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import WebPushSubscription
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("PushResource",)


class _PushSubscriptionKeys(TypedDict, total=False):
    p256dh: str
    auth: str


class _PushSubscriptionData(TypedDict, total=False):
    endpoint: str
    keys: _PushSubscriptionKeys
    standard: bool


class _PushAlerts(TypedDict, total=False):
    mention: bool
    quote: bool
    status: bool
    reblog: bool
    follow: bool
    follow_request: bool
    favourite: bool
    poll: bool
    update: bool


class _PushData(TypedDict, total=False):
    alerts: _PushAlerts
    policy: str


class _CreatePushBody(TypedDict, total=False):
    subscription: _PushSubscriptionData
    data: _PushData


class _UpdatePushBody(TypedDict, total=False):
    data: _PushData


class _SubscriptionResource:
    __slots__ = ("delete", "get", "post", "put")

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[WebPushSubscription, None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/push/subscription",
            WebPushSubscription,
            requires="2.4.0",
        )
        self.post: HttpMethod[WebPushSubscription, None, _CreatePushBody] = HttpMethod(
            client,
            "POST",
            "/api/v1/push/subscription",
            WebPushSubscription,
            requires="2.4.0",
        )
        self.put: HttpMethod[WebPushSubscription, None, _UpdatePushBody] = HttpMethod(
            client,
            "PUT",
            "/api/v1/push/subscription",
            WebPushSubscription,
            requires="2.4.0",
        )
        self.delete: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "DELETE",
            "/api/v1/push/subscription",
            dict,
            requires="2.4.0",
        )


class PushResource:
    __slots__ = ("subscription",)

    def __init__(self, client: Amasto, /) -> None:
        self.subscription = _SubscriptionResource(client)
