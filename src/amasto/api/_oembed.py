from __future__ import annotations

from .._resource import HttpMethod
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from .._client import Amasto

__all__ = ("OEmbedResource",)


class _OEmbedParams(TypedDict, total=False):
    url: str
    maxwidth: int
    maxheight: int


class OEmbedResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[dict, _OEmbedParams, None] = HttpMethod(
            client,
            "GET",
            "/api/oembed",
            dict,
            requires="1.0.0",
        )
