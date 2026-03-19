from __future__ import annotations

from ..._endpoint import Endpoint, EndpointTemplate
from ..._params import PaginationParams
from ...models.v1 import Status
from typing import TypedDict

__all__ = ("timelines",)


class _PublicTimelineParams(TypedDict, total=False):
    local: bool
    remote: bool
    only_media: bool
    max_id: str
    since_id: str
    min_id: str
    limit: int


class _TagTimelineParams(TypedDict, total=False):
    any: list[str]
    all: list[str]
    none: list[str]
    local: bool
    remote: bool
    only_media: bool
    max_id: str
    since_id: str
    min_id: str
    limit: int


class _LinkTimelineParams(TypedDict, total=False):
    url: str
    max_id: str
    since_id: str
    min_id: str
    limit: int


class _TimelinesNamespace:
    __slots__ = ()

    get_public: Endpoint[list[Status], _PublicTimelineParams, None] = Endpoint(
        "GET",
        "/api/v1/timelines/public",
        list[Status],
        params=_PublicTimelineParams,
    )
    get_home: Endpoint[list[Status], PaginationParams, None] = Endpoint(
        "GET",
        "/api/v1/timelines/home",
        list[Status],
        params=PaginationParams,
    )
    get_link: Endpoint[list[Status], _LinkTimelineParams, None] = Endpoint(
        "GET",
        "/api/v1/timelines/link",
        list[Status],
        params=_LinkTimelineParams,
        requires="4.3.0",
    )
    get_direct: Endpoint[list[Status], PaginationParams, None] = Endpoint(
        "GET",
        "/api/v1/timelines/direct",
        list[Status],
        params=PaginationParams,
    )
    get_tag: EndpointTemplate[list[Status], _TagTimelineParams, None] = EndpointTemplate(
        "GET",
        "/api/v1/timelines/tag/{hashtag}",
        list[Status],
        params=_TagTimelineParams,
    )
    get_list: EndpointTemplate[list[Status], PaginationParams, None] = EndpointTemplate(
        "GET",
        "/api/v1/timelines/list/{list_id}",
        list[Status],
        params=PaginationParams,
        requires="2.1.0",
    )


timelines = _TimelinesNamespace()
