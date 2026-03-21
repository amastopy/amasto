from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import FeaturedTag, Tag
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("FeaturedTagsResource",)


class _CreateFeaturedTagBody(TypedDict):
    name: str


class _SuggestionsResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[Tag], None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/featured_tags/suggestions",
            list[Tag],
            requires="3.3.0",
        )


class _FeaturedTagByIdResource:
    __slots__ = ("delete",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.delete: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "DELETE",
            f"/api/v1/featured_tags/{id}",
            dict,
            requires="3.3.0",
        )


class FeaturedTagsResource:
    __slots__ = ("_client", "get", "post", "suggestions")

    def __init__(self, client: Amasto, /) -> None:
        self._client = client
        self.get: HttpMethod[list[FeaturedTag], None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/featured_tags",
            list[FeaturedTag],
            requires="3.3.0",
        )
        self.post: HttpMethod[FeaturedTag, None, _CreateFeaturedTagBody] = HttpMethod(
            client,
            "POST",
            "/api/v1/featured_tags",
            FeaturedTag,
            requires="3.3.0",
        )
        self.suggestions = _SuggestionsResource(client)

    def __getitem__(self, id: str) -> _FeaturedTagByIdResource:
        return _FeaturedTagByIdResource(self._client, id)
