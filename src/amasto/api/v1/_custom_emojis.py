from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import CustomEmoji
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("CustomEmojisResource",)


class CustomEmojisResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[CustomEmoji], None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/custom_emojis",
            list[CustomEmoji],
            requires="2.0.1",
        )
