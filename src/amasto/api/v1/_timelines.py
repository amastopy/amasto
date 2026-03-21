from __future__ import annotations

from ..._params import PaginationParams
from ..._resource import HttpMethod
from ...models.v1 import Status
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("TimelinesResource",)


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


class _PublicResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[Status], _PublicTimelineParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/timelines/public",
            list[Status],
        )


class _HomeResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[Status], PaginationParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/timelines/home",
            list[Status],
        )


class _LinkResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[Status], _LinkTimelineParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/timelines/link",
            list[Status],
            requires="4.3.0",
        )


class _DirectResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[Status], PaginationParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/timelines/direct",
            list[Status],
        )


class _TagByHashtagResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, hashtag: str, /) -> None:
        self.get: HttpMethod[list[Status], _TagTimelineParams, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/timelines/tag/{hashtag}",
            list[Status],
        )


class _TimelineTagNamespace:
    __slots__ = ("_client",)

    def __init__(self, client: Amasto, /) -> None:
        self._client = client

    def __getitem__(self, hashtag: str) -> _TagByHashtagResource:
        return _TagByHashtagResource(self._client, hashtag)


class _ListByIdResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[list[Status], PaginationParams, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/timelines/list/{id}",
            list[Status],
            requires="2.1.0",
        )


class _TimelineListNamespace:
    __slots__ = ("_client",)

    def __init__(self, client: Amasto, /) -> None:
        self._client = client

    def __getitem__(self, id: str) -> _ListByIdResource:
        return _ListByIdResource(self._client, id)


class TimelinesResource:
    __slots__ = ("direct", "home", "link", "list", "public", "tag")

    def __init__(self, client: Amasto, /) -> None:
        self.public = _PublicResource(client)
        self.home = _HomeResource(client)
        self.link = _LinkResource(client)
        self.direct = _DirectResource(client)
        self.tag = _TimelineTagNamespace(client)
        self.list = _TimelineListNamespace(client)
