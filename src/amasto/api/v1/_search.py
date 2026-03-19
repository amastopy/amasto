from __future__ import annotations

from ..._endpoint import Endpoint
from ...models.v1 import Search
from typing import TypedDict

__all__ = ("get_search",)


class _SearchParams(TypedDict, total=False):
    q: str
    resolve: bool
    limit: int
    offset: int
    following: bool


get_search: Endpoint[Search, _SearchParams, None] = Endpoint(
    "GET",
    "/api/v1/search",
    Search,
    params=_SearchParams,
)
