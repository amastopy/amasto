from __future__ import annotations

from ..._endpoint import Endpoint
from ...models.v1 import Marker
from typing import TypedDict

__all__ = ("get_markers", "post_markers")


class _GetMarkersParams(TypedDict, total=False):
    timeline: list[str]


class _MarkerTimeline(TypedDict, total=False):
    last_read_id: str


class _PostMarkersBody(TypedDict, total=False):
    home: _MarkerTimeline
    notifications: _MarkerTimeline


get_markers: Endpoint[dict[str, Marker], _GetMarkersParams, None] = Endpoint(
    "GET",
    "/api/v1/markers",
    dict[str, Marker],
    params=_GetMarkersParams,
    requires="2.6.0",
)

post_markers: Endpoint[dict[str, Marker], None, _PostMarkersBody] = Endpoint(
    "POST",
    "/api/v1/markers",
    dict[str, Marker],
    body=_PostMarkersBody,
    requires="2.6.0",
)
