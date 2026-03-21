from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import Account
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("SuggestionsResource",)


class _SuggestionsParams(TypedDict, total=False):
    limit: int


class _SuggestionByIdResource:
    __slots__ = ("delete",)

    def __init__(self, client: Amasto, account_id: str, /) -> None:
        self.delete: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "DELETE",
            f"/api/v1/suggestions/{account_id}",
            dict,
            requires="2.4.3",
        )


class SuggestionsResource:
    __slots__ = ("_client", "get")

    def __init__(self, client: Amasto, /) -> None:
        self._client = client
        self.get: HttpMethod[list[Account], _SuggestionsParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/suggestions",
            list[Account],
            requires="2.4.3",
        )

    def __getitem__(self, account_id: str) -> _SuggestionByIdResource:
        return _SuggestionByIdResource(self._client, account_id)
