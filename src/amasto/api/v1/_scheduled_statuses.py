from __future__ import annotations

from ..._params import PaginationParams
from ..._resource import HttpMethod
from ...models.v1 import ScheduledStatus
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("ScheduledStatusesResource",)


class _UpdateScheduledStatusBody(TypedDict, total=False):
    scheduled_at: str


class _ScheduledStatusByIdResource:
    __slots__ = ("delete", "get", "put")

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[ScheduledStatus, None, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/scheduled_statuses/{id}",
            ScheduledStatus,
            requires="2.7.0",
        )
        self.put: HttpMethod[ScheduledStatus, None, _UpdateScheduledStatusBody] = HttpMethod(
            client,
            "PUT",
            f"/api/v1/scheduled_statuses/{id}",
            ScheduledStatus,
            requires="2.7.0",
        )
        self.delete: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "DELETE",
            f"/api/v1/scheduled_statuses/{id}",
            dict,
            requires="2.7.0",
        )


class ScheduledStatusesResource:
    __slots__ = ("_client", "get")

    def __init__(self, client: Amasto, /) -> None:
        self._client = client
        self.get: HttpMethod[list[ScheduledStatus], PaginationParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/scheduled_statuses",
            list[ScheduledStatus],
            requires="2.7.0",
        )

    def __getitem__(self, id: str) -> _ScheduledStatusByIdResource:
        return _ScheduledStatusByIdResource(self._client, id)
