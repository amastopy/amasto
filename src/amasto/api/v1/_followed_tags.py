from __future__ import annotations

from ..._endpoint import Endpoint
from ..._params import PaginationParams
from ...models.v1 import Tag

__all__ = ("get_followed_tags",)

get_followed_tags: Endpoint[list[Tag], PaginationParams, None] = Endpoint(
    "GET",
    "/api/v1/followed_tags",
    list[Tag],
    params=PaginationParams,
    requires="4.3.0",
)
