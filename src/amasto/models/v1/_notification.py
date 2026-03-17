from __future__ import annotations

from ._account import Account
from ._account_warning import AccountWarning
from ._relationship_severance_event import RelationshipSeveranceEvent
from ._report import Report
from ._status import Status
from amasto._version import Unsupported, since
from pydantic import BaseModel, ConfigDict
from typing import Literal

__all__ = ("Notification",)

_NOTIFICATION_TYPE = Literal[
    "mention",
    "status",
    "reblog",
    "follow",
    "follow_request",
    "favourite",
    "poll",
    "update",
    "admin.sign_up",
    "admin.report",
    "severed_relationships",
    "moderation_warning",
    "quote",
    "quoted_update",
]


class Notification(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    type: _NOTIFICATION_TYPE
    created_at: str
    account: Account
    status: Status | None = None
    report: Report | None | Unsupported = since("4.0.0")
    event: RelationshipSeveranceEvent | None | Unsupported = since("4.3.0")
    moderation_warning: AccountWarning | None | Unsupported = since("4.3.0")
    group_key: str | Unsupported = since("4.3.0")
