from __future__ import annotations

from ..._endpoint import Endpoint
from ...models.v1 import Suggestion
from typing import TypedDict

__all__ = ("get_suggestions",)


class _SuggestionsParams(TypedDict, total=False):
    limit: int


get_suggestions: Endpoint[list[Suggestion], _SuggestionsParams, None] = Endpoint(
    "GET",
    "/api/v2/suggestions",
    list[Suggestion],
    params=_SuggestionsParams,
    requires="3.4.0",
)
