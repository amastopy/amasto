from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import Marker
from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("MarkersResource",)


class _GetMarkersParams(TypedDict, total=False):
    timeline: list[str | Literal["home", "notifications"]]


class _MarkerTimeline(TypedDict, total=False):
    last_read_id: str


class _PostMarkersBody(TypedDict, total=False):
    home: _MarkerTimeline
    notifications: _MarkerTimeline


class MarkersResource:
    __slots__ = ("get", "post")

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[dict[str, Marker], _GetMarkersParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/markers",
            dict[str, Marker],
            requires="2.6.0",
        )
        self.post: HttpMethod[dict[str, Marker], None, _PostMarkersBody] = HttpMethod(
            client,
            "POST",
            "/api/v1/markers",
            dict[str, Marker],
            requires="2.6.0",
        )
