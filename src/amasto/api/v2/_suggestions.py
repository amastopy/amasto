from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import Suggestion
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("SuggestionsResource",)


class _SuggestionsParams(TypedDict, total=False):
    limit: int


class SuggestionsResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[Suggestion], _SuggestionsParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v2/suggestions",
            list[Suggestion],
            requires="3.4.0",
        )
