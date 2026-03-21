from __future__ import annotations

from .._resource import HttpMethod
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from .._client import Amasto

__all__ = ("RevokeResource",)


class _RevokeBody(TypedDict, total=False):
    client_id: str
    client_secret: str
    token: str


class RevokeResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, /) -> None:
        self.post: HttpMethod[dict, None, _RevokeBody] = HttpMethod(
            client,
            "POST",
            "/oauth/revoke",
            dict,
            requires="1.5.0",
        )
