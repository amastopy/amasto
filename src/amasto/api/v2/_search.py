from __future__ import annotations

from ..._endpoint import Endpoint
from ...models.v1 import Search
from typing import TypedDict

__all__ = ("get_search",)


class _SearchParams(TypedDict, total=False):
    q: str
    type: str
    resolve: bool
    following: bool
    account_id: str
    exclude_unreviewed: bool
    max_id: str
    min_id: str
    limit: int
    offset: int


get_search: Endpoint[Search, _SearchParams, None] = Endpoint(
    "GET",
    "/api/v2/search",
    Search,
    params=_SearchParams,
    requires="2.4.1",
)
