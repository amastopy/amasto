from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import Announcement
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("AnnouncementsResource",)


class _AnnouncementReactionResource:
    __slots__ = ("delete", "put")

    def __init__(self, client: Amasto, id: str, name: str, /) -> None:
        self.put: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "PUT",
            f"/api/v1/announcements/{id}/reactions/{name}",
            dict,
            requires="3.1.0",
        )
        self.delete: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "DELETE",
            f"/api/v1/announcements/{id}/reactions/{name}",
            dict,
            requires="3.1.0",
        )


class _AnnouncementReactionsNamespace:
    __slots__ = ("_client", "_id")

    def __init__(self, client: Amasto, id: str, /) -> None:
        self._client = client
        self._id = id

    def __getitem__(self, name: str) -> _AnnouncementReactionResource:
        return _AnnouncementReactionResource(self._client, self._id, name)


class _DismissResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/announcements/{id}/dismiss",
            dict,
            requires="3.1.0",
        )


class _AnnouncementByIdResource:
    __slots__ = ("dismiss", "reactions")

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.dismiss = _DismissResource(client, id)
        self.reactions = _AnnouncementReactionsNamespace(client, id)


class AnnouncementsResource:
    __slots__ = ("_client", "get")

    def __init__(self, client: Amasto, /) -> None:
        self._client = client
        self.get: HttpMethod[list[Announcement], None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/announcements",
            list[Announcement],
            requires="3.1.0",
        )

    def __getitem__(self, id: str) -> _AnnouncementByIdResource:
        return _AnnouncementByIdResource(self._client, id)
