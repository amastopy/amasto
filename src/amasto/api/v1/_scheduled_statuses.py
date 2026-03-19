from __future__ import annotations

from ..._endpoint import EndpointTemplate, SubscriptableEndpoint
from ..._params import PaginationParams
from ...models.v1 import ScheduledStatus
from typing import TypedDict

__all__ = ("delete_scheduled_statuses", "get_scheduled_statuses", "put_scheduled_statuses")


class _UpdateScheduledStatusBody(TypedDict, total=False):
    scheduled_at: str


get_scheduled_statuses: SubscriptableEndpoint[list[ScheduledStatus], PaginationParams, None, ScheduledStatus] = (
    SubscriptableEndpoint(
        "GET",
        "/api/v1/scheduled_statuses",
        list[ScheduledStatus],
        "/api/v1/scheduled_statuses/{id}",
        ScheduledStatus,
        params=PaginationParams,
        requires="2.7.0",
        item_requires="2.7.0",
    )
)

put_scheduled_statuses: EndpointTemplate[ScheduledStatus, None, _UpdateScheduledStatusBody] = EndpointTemplate(
    "PUT",
    "/api/v1/scheduled_statuses/{id}",
    ScheduledStatus,
    body=_UpdateScheduledStatusBody,
    requires="2.7.0",
)

delete_scheduled_statuses: EndpointTemplate[dict, None, None] = EndpointTemplate(
    "DELETE",
    "/api/v1/scheduled_statuses/{id}",
    dict,
    requires="2.7.0",
)
