from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import Preferences
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("PreferencesResource",)


class PreferencesResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[Preferences, None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/preferences",
            Preferences,
            requires="2.8.0",
        )
