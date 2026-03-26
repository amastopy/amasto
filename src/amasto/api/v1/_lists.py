from __future__ import annotations

from ..._pagination import PaginatedHttpMethod
from ..._params import PaginationParams
from ..._resource import HttpMethod
from ...models.v1 import Account, List
from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("ListsResource",)


class _CreateListBody(TypedDict, total=False):
    title: str
    replies_policy: str | Literal["followed", "list", "none"]
    exclusive: bool


class _UpdateListBody(TypedDict, total=False):
    title: str
    replies_policy: str | Literal["followed", "list", "none"]
    exclusive: bool


class _ListAccountsBody(TypedDict):
    account_ids: list[str]


class _ListAccountsResource:
    __slots__ = ("delete", "get", "post")

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: PaginatedHttpMethod[Account, PaginationParams] = PaginatedHttpMethod(
            client,
            "GET",
            f"/api/v1/lists/{id}/accounts",
            Account,
            requires="2.1.0",
        )
        self.post: HttpMethod[dict, None, _ListAccountsBody] = HttpMethod(
            client,
            "POST",
            f"/api/v1/lists/{id}/accounts",
            dict,
            requires="2.1.0",
        )
        self.delete: HttpMethod[dict, None, _ListAccountsBody] = HttpMethod(
            client,
            "DELETE",
            f"/api/v1/lists/{id}/accounts",
            dict,
            requires="2.1.0",
        )


class _ListByIdResource:
    __slots__ = ("accounts", "delete", "get", "put")

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[List, None, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/lists/{id}",
            List,
            requires="2.1.0",
        )
        self.put: HttpMethod[List, None, _UpdateListBody] = HttpMethod(
            client,
            "PUT",
            f"/api/v1/lists/{id}",
            List,
            requires="2.1.0",
        )
        self.delete: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "DELETE",
            f"/api/v1/lists/{id}",
            dict,
            requires="2.1.0",
        )
        self.accounts = _ListAccountsResource(client, id)


class ListsResource:
    __slots__ = ("_client", "get", "post")

    def __init__(self, client: Amasto, /) -> None:
        self._client = client
        self.get: HttpMethod[list[List], None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/lists",
            list[List],
            requires="2.1.0",
        )
        self.post: HttpMethod[List, None, _CreateListBody] = HttpMethod(
            client,
            "POST",
            "/api/v1/lists",
            List,
            requires="2.1.0",
        )

    def __getitem__(self, id: str) -> _ListByIdResource:
        return _ListByIdResource(self._client, id)
