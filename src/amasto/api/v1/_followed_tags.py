from __future__ import annotations

from ..._params import PaginationParams
from ..._resource import HttpMethod
from ...models.v1 import Tag
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("FollowedTagsResource",)


class FollowedTagsResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[Tag], PaginationParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/followed_tags",
            list[Tag],
            requires="4.3.0",
        )
