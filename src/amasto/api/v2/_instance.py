from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v2 import Instance
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("InstanceResource",)


class InstanceResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[Instance, None, None] = HttpMethod(
            client,
            "GET",
            "/api/v2/instance",
            Instance,
            requires="3.4.0",
        )
