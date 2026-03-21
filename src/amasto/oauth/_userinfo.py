from __future__ import annotations

from .._resource import HttpMethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .._client import Amasto

__all__ = ("UserinfoResource",)


class UserinfoResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "GET",
            "/oauth/userinfo",
            dict,
        )
