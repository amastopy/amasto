from __future__ import annotations

from amasto._version import Unsupported, since, unsupported
from pydantic import BaseModel, ConfigDict, Field

__all__ = ("WebPushAlerts", "WebPushSubscription")


@since("2.4.0")
class WebPushAlerts(BaseModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    mention: bool
    reblog: bool
    follow: bool
    favourite: bool
    poll: bool | Unsupported = since("2.8.0")
    follow_request: bool | Unsupported = since("3.1.0")
    status: bool | Unsupported = since("3.3.0")
    update: bool | Unsupported = since("3.5.0")
    admin_sign_up: bool | Unsupported = Field(default=unsupported, alias="admin.sign_up")
    admin_report: bool | Unsupported = Field(default=unsupported, alias="admin.report")


@since("2.4.0")
class WebPushSubscription(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    endpoint: str
    server_key: str
    alerts: WebPushAlerts
    standard: bool | Unsupported = since("4.4.0")
