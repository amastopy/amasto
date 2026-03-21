from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import Status, Tag, TrendsLink
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("TrendsResource",)


class _TrendsParams(TypedDict, total=False):
    limit: int
    offset: int


class _TrendsTagsResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[Tag], _TrendsParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/trends/tags",
            list[Tag],
            requires="3.0.0",
        )


class _TrendsStatusesResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[Status], _TrendsParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/trends/statuses",
            list[Status],
            requires="3.5.0",
        )


class _TrendsLinksResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[TrendsLink], _TrendsParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/trends/links",
            list[TrendsLink],
            requires="3.5.0",
        )


class TrendsResource:
    __slots__ = ("links", "statuses", "tags")

    def __init__(self, client: Amasto, /) -> None:
        self.tags = _TrendsTagsResource(client)
        self.statuses = _TrendsStatusesResource(client)
        self.links = _TrendsLinksResource(client)
