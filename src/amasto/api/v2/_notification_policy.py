from __future__ import annotations

from ..._endpoint import Endpoint
from ...models.v2 import NotificationPolicy
from typing import TypedDict

__all__ = ("notification_policy",)


class _UpdatePolicyBody(TypedDict, total=False):
    for_not_following: str
    for_not_followers: str
    for_new_accounts: str
    for_private_mentions: str
    for_limited_accounts: str


class _NotificationPolicyNamespace:
    __slots__ = ()

    get = Endpoint("GET", "/api/v2/notifications/policy", NotificationPolicy, requires="4.3.0")
    patch: Endpoint[NotificationPolicy, None, _UpdatePolicyBody] = Endpoint(
        "PATCH",
        "/api/v2/notifications/policy",
        NotificationPolicy,
        body=_UpdatePolicyBody,
        requires="4.3.0",
    )


notification_policy = _NotificationPolicyNamespace()
