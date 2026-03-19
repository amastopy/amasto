from __future__ import annotations

from ..._endpoint import Endpoint, EndpointTemplate, SubscriptableEndpoint
from ..._params import PaginationParams
from ...models.v1 import Account, List
from typing import TypedDict

__all__ = ("delete_lists", "get_lists", "lists", "post_lists", "put_lists")


class _CreateListBody(TypedDict, total=False):
    title: str
    replies_policy: str
    exclusive: bool


class _UpdateListBody(TypedDict, total=False):
    title: str
    replies_policy: str
    exclusive: bool


class _ListAccountsBody(TypedDict):
    account_ids: list[str]


get_lists: SubscriptableEndpoint[list[List], None, None, List] = SubscriptableEndpoint(
    "GET",
    "/api/v1/lists",
    list[List],
    "/api/v1/lists/{id}",
    List,
    requires="2.1.0",
    item_requires="2.1.0",
)

post_lists: Endpoint[List, None, _CreateListBody] = Endpoint(
    "POST",
    "/api/v1/lists",
    List,
    body=_CreateListBody,
    requires="2.1.0",
)

put_lists: EndpointTemplate[List, None, _UpdateListBody] = EndpointTemplate(
    "PUT",
    "/api/v1/lists/{id}",
    List,
    body=_UpdateListBody,
    requires="2.1.0",
)

delete_lists: EndpointTemplate[dict, None, None] = EndpointTemplate(
    "DELETE",
    "/api/v1/lists/{id}",
    dict,
    requires="2.1.0",
)


class _ListsById:
    __slots__ = ("delete_accounts", "get_accounts", "post_accounts")

    def __init__(self, id: str, /) -> None:
        self.get_accounts: Endpoint[list[Account], PaginationParams, None] = Endpoint(
            "GET",
            f"/api/v1/lists/{id}/accounts",
            list[Account],
            params=PaginationParams,
            requires="2.1.0",
        )
        self.post_accounts: Endpoint[dict, None, _ListAccountsBody] = Endpoint(
            "POST",
            f"/api/v1/lists/{id}/accounts",
            dict,
            body=_ListAccountsBody,
            requires="2.1.0",
        )
        self.delete_accounts: Endpoint[dict, None, _ListAccountsBody] = Endpoint(
            "DELETE",
            f"/api/v1/lists/{id}/accounts",
            dict,
            body=_ListAccountsBody,
            requires="2.1.0",
        )


class _ListsNamespace:
    __slots__ = ()

    def __getitem__(self, id: str) -> _ListsById:
        return _ListsById(id)


lists = _ListsNamespace()
