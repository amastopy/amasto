from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import Tag
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("TagsResource",)


class _FollowResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, key: str, /) -> None:
        self.post: HttpMethod[Tag, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/tags/{key}/follow",
            Tag,
            requires="4.0.0",
        )


class _UnfollowResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, key: str, /) -> None:
        self.post: HttpMethod[Tag, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/tags/{key}/unfollow",
            Tag,
            requires="4.0.0",
        )


class _FeatureResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, key: str, /) -> None:
        self.post: HttpMethod[Tag, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/tags/{key}/feature",
            Tag,
            requires="4.4.0",
        )


class _UnfeatureResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, key: str, /) -> None:
        self.post: HttpMethod[Tag, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/tags/{key}/unfeature",
            Tag,
            requires="4.4.0",
        )


class _TagByKeyResource:
    __slots__ = ("feature", "follow", "get", "unfeature", "unfollow")

    def __init__(self, client: Amasto, key: str, /) -> None:
        self.get: HttpMethod[Tag, None, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/tags/{key}",
            Tag,
            requires="4.0.0",
        )
        self.follow = _FollowResource(client, key)
        self.unfollow = _UnfollowResource(client, key)
        self.feature = _FeatureResource(client, key)
        self.unfeature = _UnfeatureResource(client, key)


class TagsResource:
    __slots__ = ("_client",)

    def __init__(self, client: Amasto, /) -> None:
        self._client = client

    def __getitem__(self, key: str) -> _TagByKeyResource:
        return _TagByKeyResource(self._client, key)
