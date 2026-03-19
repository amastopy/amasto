from __future__ import annotations

from ..._endpoint import Endpoint, EndpointTemplate
from ...models.v1 import Announcement

__all__ = ("announcements", "get_announcements")


get_announcements: Endpoint[list[Announcement], None, None] = Endpoint(
    "GET",
    "/api/v1/announcements",
    list[Announcement],
    requires="3.1.0",
)


class _AnnouncementsById:
    __slots__ = ("delete_reactions", "post_dismiss", "put_reactions")

    def __init__(self, id: str, /) -> None:
        self.post_dismiss = Endpoint("POST", f"/api/v1/announcements/{id}/dismiss", dict, requires="3.1.0")
        self.put_reactions: EndpointTemplate[dict, None, None] = EndpointTemplate(
            "PUT",
            f"/api/v1/announcements/{id}/reactions/{{name}}",
            dict,
            requires="3.1.0",
        )
        self.delete_reactions: EndpointTemplate[dict, None, None] = EndpointTemplate(
            "DELETE",
            f"/api/v1/announcements/{id}/reactions/{{name}}",
            dict,
            requires="3.1.0",
        )


class _AnnouncementsNamespace:
    __slots__ = ()

    def __getitem__(self, id: str) -> _AnnouncementsById:
        return _AnnouncementsById(id)


announcements = _AnnouncementsNamespace()
