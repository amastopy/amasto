from __future__ import annotations

from ..._endpoint import Endpoint
from ...models.v1 import CustomEmoji

__all__ = ("get_custom_emojis",)

get_custom_emojis: Endpoint[list[CustomEmoji], None, None] = Endpoint(
    "GET",
    "/api/v1/custom_emojis",
    list[CustomEmoji],
    requires="2.0.1",
)
