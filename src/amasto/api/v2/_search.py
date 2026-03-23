from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import Search
from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("SearchResource",)


class _SearchParams(TypedDict, total=False):
    q: str
    type: str | Literal["accounts", "hashtags", "statuses"]
    resolve: bool
    following: bool
    account_id: str
    exclude_unreviewed: bool
    max_id: str
    min_id: str
    limit: int
    offset: int


class SearchResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[Search, _SearchParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v2/search",
            Search,
            requires="2.4.1",
        )
