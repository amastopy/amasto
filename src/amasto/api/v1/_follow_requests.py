from __future__ import annotations

from ..._endpoint import Endpoint
from ..._params import PaginationParams
from ...models.v1 import Account, Relationship

__all__ = ("follow_requests", "get_follow_requests")


get_follow_requests: Endpoint[list[Account], PaginationParams, None] = Endpoint(
    "GET",
    "/api/v1/follow_requests",
    list[Account],
    params=PaginationParams,
)


class _FollowRequestsById:
    __slots__ = ("post_authorize", "post_reject")

    def __init__(self, account_id: str, /) -> None:
        self.post_authorize = Endpoint(
            "POST",
            f"/api/v1/follow_requests/{account_id}/authorize",
            Relationship,
        )
        self.post_reject = Endpoint(
            "POST",
            f"/api/v1/follow_requests/{account_id}/reject",
            Relationship,
        )


class _FollowRequestsNamespace:
    __slots__ = ()

    def __getitem__(self, account_id: str) -> _FollowRequestsById:
        return _FollowRequestsById(account_id)


follow_requests = _FollowRequestsNamespace()
