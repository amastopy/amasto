from __future__ import annotations

from .._endpoint import Endpoint
from typing import TypedDict

__all__ = ("get_oembed",)


class _OEmbedParams(TypedDict, total=False):
    url: str
    maxwidth: int
    maxheight: int


get_oembed: Endpoint[dict, _OEmbedParams, None] = Endpoint(
    "GET",
    "/api/oembed",
    dict,
    params=_OEmbedParams,
    requires="1.0.0",
)
