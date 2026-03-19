from __future__ import annotations

from ..._endpoint import Endpoint
from ..._params import PaginationParams
from ...models.v1 import Status

__all__ = ("get_favourites",)

get_favourites: Endpoint[list[Status], PaginationParams, None] = Endpoint(
    "GET",
    "/api/v1/favourites",
    list[Status],
    params=PaginationParams,
)
