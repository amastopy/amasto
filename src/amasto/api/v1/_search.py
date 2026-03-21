from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import Search
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("SearchResource",)


class _SearchParams(TypedDict, total=False):
    q: str
    resolve: bool
    limit: int
    offset: int
    following: bool


class SearchResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[Search, _SearchParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/search",
            Search,
        )
