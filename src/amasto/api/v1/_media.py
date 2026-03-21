from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import MediaAttachment
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("MediaResource",)


class _UpdateMediaBody(TypedDict, total=False):
    description: str
    focus: str


class _MediaByIdResource:
    __slots__ = ("delete", "get", "put")

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[MediaAttachment, None, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/media/{id}",
            MediaAttachment,
        )
        self.put: HttpMethod[MediaAttachment, None, _UpdateMediaBody] = HttpMethod(
            client,
            "PUT",
            f"/api/v1/media/{id}",
            MediaAttachment,
        )
        self.delete: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "DELETE",
            f"/api/v1/media/{id}",
            dict,
            requires="4.4.0",
        )


class MediaResource:
    __slots__ = ("_client",)

    def __init__(self, client: Amasto, /) -> None:
        self._client = client

    def __getitem__(self, id: str) -> _MediaByIdResource:
        return _MediaByIdResource(self._client, id)
