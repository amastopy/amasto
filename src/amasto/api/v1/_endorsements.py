from __future__ import annotations

from ..._endpoint import Endpoint
from ..._params import PaginationParams
from ...models.v1 import Account

__all__ = ("get_endorsements",)

get_endorsements: Endpoint[list[Account], PaginationParams, None] = Endpoint(
    "GET",
    "/api/v1/endorsements",
    list[Account],
    params=PaginationParams,
    requires="2.5.0",
)
