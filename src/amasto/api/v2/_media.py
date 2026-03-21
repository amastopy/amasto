from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import MediaAttachment
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("MediaResource",)


class MediaResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, /) -> None:
        self.post: HttpMethod[MediaAttachment, None, None] = HttpMethod(
            client,
            "POST",
            "/api/v2/media",
            MediaAttachment,
            requires="3.2.0",
        )
