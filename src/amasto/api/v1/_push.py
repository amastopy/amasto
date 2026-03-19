from __future__ import annotations

from ..._endpoint import Endpoint
from ...models.v1 import WebPushSubscription
from typing import TypedDict

__all__ = ("push",)


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


class _PushNamespace:
    __slots__ = ()

    post_subscription: Endpoint[WebPushSubscription, None, _CreatePushBody] = Endpoint(
        "POST",
        "/api/v1/push/subscription",
        WebPushSubscription,
        body=_CreatePushBody,
        requires="2.4.0",
    )
    get_subscription = Endpoint("GET", "/api/v1/push/subscription", WebPushSubscription, requires="2.4.0")
    put_subscription: Endpoint[WebPushSubscription, None, _UpdatePushBody] = Endpoint(
        "PUT",
        "/api/v1/push/subscription",
        WebPushSubscription,
        body=_UpdatePushBody,
        requires="2.4.0",
    )
    delete_subscription = Endpoint("DELETE", "/api/v1/push/subscription", dict, requires="2.4.0")


push = _PushNamespace()
