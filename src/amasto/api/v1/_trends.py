from __future__ import annotations

from ..._endpoint import Endpoint
from ...models.v1 import Status, Tag, TrendsLink
from typing import TypedDict

__all__ = ("trends",)


class _TrendsParams(TypedDict, total=False):
    limit: int
    offset: int


class _TrendsNamespace:
    __slots__ = ()

    get_tags: Endpoint[list[Tag], _TrendsParams, None] = Endpoint(
        "GET",
        "/api/v1/trends/tags",
        list[Tag],
        params=_TrendsParams,
        requires="3.0.0",
    )
    get_statuses: Endpoint[list[Status], _TrendsParams, None] = Endpoint(
        "GET",
        "/api/v1/trends/statuses",
        list[Status],
        params=_TrendsParams,
        requires="3.5.0",
    )
    get_links: Endpoint[list[TrendsLink], _TrendsParams, None] = Endpoint(
        "GET",
        "/api/v1/trends/links",
        list[TrendsLink],
        params=_TrendsParams,
        requires="3.5.0",
    )


trends = _TrendsNamespace()
