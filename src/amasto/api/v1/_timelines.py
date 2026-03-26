from __future__ import annotations

from ..._pagination import PaginatedHttpMethod
from ..._params import PaginationParams
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
        self.get: PaginatedHttpMethod[Status, _PublicTimelineParams] = PaginatedHttpMethod(
            client,
            "GET",
            "/api/v1/timelines/public",
            Status,
        )


class _HomeResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: PaginatedHttpMethod[Status, PaginationParams] = PaginatedHttpMethod(
            client,
            "GET",
            "/api/v1/timelines/home",
            Status,
        )


class _LinkResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: PaginatedHttpMethod[Status, _LinkTimelineParams] = PaginatedHttpMethod(
            client,
            "GET",
            "/api/v1/timelines/link",
            Status,
            requires="4.3.0",
        )


class _DirectResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: PaginatedHttpMethod[Status, PaginationParams] = PaginatedHttpMethod(
            client,
            "GET",
            "/api/v1/timelines/direct",
            Status,
        )


class _TagByHashtagResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, hashtag: str, /) -> None:
        self.get: PaginatedHttpMethod[Status, _TagTimelineParams] = PaginatedHttpMethod(
            client,
            "GET",
            f"/api/v1/timelines/tag/{hashtag}",
            Status,
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
        self.get: PaginatedHttpMethod[Status, PaginationParams] = PaginatedHttpMethod(
            client,
            "GET",
            f"/api/v1/timelines/list/{id}",
            Status,
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
