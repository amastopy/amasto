from __future__ import annotations

from ..._params import PaginationParams
from ..._resource import HttpMethod
from ...models.v1 import Account
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("EndorsementsResource",)


class EndorsementsResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[Account], PaginationParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/endorsements",
            list[Account],
            requires="2.5.0",
        )
