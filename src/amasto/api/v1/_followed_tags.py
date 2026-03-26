from __future__ import annotations

from ..._pagination import PaginatedHttpMethod
from ..._params import PaginationParams
from ...models.v1 import Tag
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("FollowedTagsResource",)


class FollowedTagsResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: PaginatedHttpMethod[Tag, PaginationParams] = PaginatedHttpMethod(
            client,
            "GET",
            "/api/v1/followed_tags",
            Tag,
            requires="4.3.0",
        )
