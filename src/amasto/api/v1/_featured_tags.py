from __future__ import annotations

from ..._endpoint import Endpoint, EndpointTemplate
from ...models.v1 import FeaturedTag, Tag
from typing import TypedDict

__all__ = ("delete_featured_tags", "featured_tags", "get_featured_tags", "post_featured_tags")


class _CreateFeaturedTagBody(TypedDict):
    name: str


get_featured_tags: Endpoint[list[FeaturedTag], None, None] = Endpoint(
    "GET",
    "/api/v1/featured_tags",
    list[FeaturedTag],
    requires="3.3.0",
)

post_featured_tags: Endpoint[FeaturedTag, None, _CreateFeaturedTagBody] = Endpoint(
    "POST",
    "/api/v1/featured_tags",
    FeaturedTag,
    body=_CreateFeaturedTagBody,
    requires="3.3.0",
)

delete_featured_tags: EndpointTemplate[dict, None, None] = EndpointTemplate(
    "DELETE",
    "/api/v1/featured_tags/{id}",
    dict,
    requires="3.3.0",
)


class _FeaturedTagsNamespace:
    __slots__ = ()

    get_suggestions = Endpoint("GET", "/api/v1/featured_tags/suggestions", list[Tag], requires="3.3.0")


featured_tags = _FeaturedTagsNamespace()
