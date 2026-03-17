from __future__ import annotations

from amasto._version import since
from pydantic import BaseModel, ConfigDict
from typing import Literal

__all__ = ("NotificationPolicy", "NotificationPolicySummary")

_POLICY_ACTION = Literal["accept", "filter", "drop"]


@since("4.3.0")
class NotificationPolicySummary(BaseModel):
    model_config = ConfigDict(frozen=True)

    pending_requests_count: int
    pending_notifications_count: int


@since("4.3.0")
class NotificationPolicy(BaseModel):
    model_config = ConfigDict(frozen=True)

    for_not_following: _POLICY_ACTION
    for_not_followers: _POLICY_ACTION
    for_new_accounts: _POLICY_ACTION
    for_private_mentions: _POLICY_ACTION
    for_limited_accounts: _POLICY_ACTION
    summary: NotificationPolicySummary
