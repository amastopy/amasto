from __future__ import annotations

from ..._endpoint import Endpoint
from ..._params import PaginationParams
from ...models.v1 import MutedAccount

__all__ = ("get_mutes",)

get_mutes: Endpoint[list[MutedAccount], PaginationParams, None] = Endpoint(
    "GET",
    "/api/v1/mutes",
    list[MutedAccount],
    params=PaginationParams,
)
