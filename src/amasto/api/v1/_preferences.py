from __future__ import annotations

from ..._endpoint import Endpoint
from ...models.v1 import Preferences

__all__ = ("get_preferences",)

get_preferences: Endpoint[Preferences, None, None] = Endpoint(
    "GET",
    "/api/v1/preferences",
    Preferences,
    requires="2.8.0",
)
