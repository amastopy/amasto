from __future__ import annotations

from ..._endpoint import Endpoint
from ..._params import PaginationParams
from ...models.v1 import Status

__all__ = ("get_bookmarks",)

get_bookmarks: Endpoint[list[Status], PaginationParams, None] = Endpoint(
    "GET",
    "/api/v1/bookmarks",
    list[Status],
    params=PaginationParams,
    requires="3.1.0",
)
