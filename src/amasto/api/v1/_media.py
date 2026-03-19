from __future__ import annotations

from ..._endpoint import EndpointTemplate
from ...models.v1 import MediaAttachment
from typing import TypedDict

__all__ = ("delete_media", "get_media", "put_media")


class _UpdateMediaBody(TypedDict, total=False):
    description: str
    focus: str


get_media: EndpointTemplate[MediaAttachment, None, None] = EndpointTemplate(
    "GET",
    "/api/v1/media/{id}",
    MediaAttachment,
)

put_media: EndpointTemplate[MediaAttachment, None, _UpdateMediaBody] = EndpointTemplate(
    "PUT",
    "/api/v1/media/{id}",
    MediaAttachment,
    body=_UpdateMediaBody,
)

delete_media: EndpointTemplate[dict, None, None] = EndpointTemplate(
    "DELETE",
    "/api/v1/media/{id}",
    dict,
    requires="4.4.0",
)
