from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .._client import Amasto

__all__ = ("ApiNamespace",)


class ApiNamespace:
    __slots__ = ("oembed", "v1", "v2")

    def __init__(self, client: Amasto, /) -> None:
        from ._oembed import OEmbedResource
        from .v1 import V1Namespace
        from .v2 import V2Namespace

        self.v1 = V1Namespace(client)
        self.v2 = V2Namespace(client)
        self.oembed = OEmbedResource(client)
