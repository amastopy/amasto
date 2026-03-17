from __future__ import annotations

from amasto._version import since
from pydantic import BaseModel, ConfigDict

__all__ = ("NotificationPolicy", "NotificationPolicySummary")


@since("4.3.0")
class NotificationPolicySummary(BaseModel):
    model_config = ConfigDict(frozen=True)

    pending_requests_count: int
    pending_notifications_count: int


@since("4.3.0")
class NotificationPolicy(BaseModel):
    model_config = ConfigDict(frozen=True)

    filter_not_following: bool
    filter_not_followers: bool
    filter_new_accounts: bool
    filter_private_mentions: bool
    summary: NotificationPolicySummary
