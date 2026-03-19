from __future__ import annotations

from ..._endpoint import Endpoint
from ..._params import PaginationParams
from ...models.v1 import Account

__all__ = ("get_blocks",)

get_blocks: Endpoint[list[Account], PaginationParams, None] = Endpoint(
    "GET",
    "/api/v1/blocks",
    list[Account],
    params=PaginationParams,
)
