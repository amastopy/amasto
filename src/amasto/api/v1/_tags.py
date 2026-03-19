from __future__ import annotations

from ..._endpoint import Endpoint, EndpointTemplate
from ...models.v1 import Tag

__all__ = ("get_tags", "tags")


get_tags: EndpointTemplate[Tag, None, None] = EndpointTemplate(
    "GET",
    "/api/v1/tags/{name}",
    Tag,
    requires="4.0.0",
)


class _TagsByName:
    __slots__ = ("post_follow", "post_unfollow")

    def __init__(self, name: str, /) -> None:
        self.post_follow = Endpoint("POST", f"/api/v1/tags/{name}/follow", Tag, requires="4.0.0")
        self.post_unfollow = Endpoint("POST", f"/api/v1/tags/{name}/unfollow", Tag, requires="4.0.0")


class _TagsById:
    __slots__ = ("post_feature", "post_unfeature")

    def __init__(self, id: str, /) -> None:
        self.post_feature = Endpoint("POST", f"/api/v1/tags/{id}/feature", Tag, requires="4.4.0")
        self.post_unfeature = Endpoint("POST", f"/api/v1/tags/{id}/unfeature", Tag, requires="4.4.0")


class _TagsNamespace:
    __slots__ = ()

    def by_name(self, name: str) -> _TagsByName:
        return _TagsByName(name)

    def __getitem__(self, id: str) -> _TagsById:
        return _TagsById(id)


tags = _TagsNamespace()
