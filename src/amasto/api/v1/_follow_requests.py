from __future__ import annotations

from ..._params import PaginationParams
from ..._resource import HttpMethod
from ...models.v1 import Account, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("FollowRequestsResource",)


class _AuthorizeResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, account_id: str, /) -> None:
        self.post: HttpMethod[Relationship, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/follow_requests/{account_id}/authorize",
            Relationship,
        )


class _RejectResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, account_id: str, /) -> None:
        self.post: HttpMethod[Relationship, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/follow_requests/{account_id}/reject",
            Relationship,
        )


class _FollowRequestByIdResource:
    __slots__ = ("authorize", "reject")

    def __init__(self, client: Amasto, account_id: str, /) -> None:
        self.authorize = _AuthorizeResource(client, account_id)
        self.reject = _RejectResource(client, account_id)


class FollowRequestsResource:
    __slots__ = ("_client", "get")

    def __init__(self, client: Amasto, /) -> None:
        self._client = client
        self.get: HttpMethod[list[Account], PaginationParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/follow_requests",
            list[Account],
        )

    def __getitem__(self, account_id: str) -> _FollowRequestByIdResource:
        return _FollowRequestByIdResource(self._client, account_id)
