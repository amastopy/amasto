from __future__ import annotations

from ..._pagination import PaginatedHttpMethod
from ..._params import PaginationParams
from ...models.v1 import Status
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("BookmarksResource",)


class BookmarksResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: PaginatedHttpMethod[Status, PaginationParams] = PaginatedHttpMethod(
            client,
            "GET",
            "/api/v1/bookmarks",
            Status,
            requires="3.1.0",
        )
