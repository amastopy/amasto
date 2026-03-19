from __future__ import annotations

from ..._endpoint import Endpoint, EndpointTemplate
from ...models.v1 import Account
from typing import TypedDict

__all__ = ("delete_suggestions", "get_suggestions")


class _SuggestionsParams(TypedDict, total=False):
    limit: int


get_suggestions: Endpoint[list[Account], _SuggestionsParams, None] = Endpoint(
    "GET",
    "/api/v1/suggestions",
    list[Account],
    params=_SuggestionsParams,
    requires="2.4.3",
)

delete_suggestions: EndpointTemplate[dict, None, None] = EndpointTemplate(
    "DELETE",
    "/api/v1/suggestions/{account_id}",
    dict,
    requires="2.4.3",
)
