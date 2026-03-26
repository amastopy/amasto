from __future__ import annotations

from ..._pagination import PaginatedHttpMethod
from ..._params import PaginationParams
from ...models.v1 import MutedAccount
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("MutesResource",)


class MutesResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: PaginatedHttpMethod[MutedAccount, PaginationParams] = PaginatedHttpMethod(
            client,
            "GET",
            "/api/v1/mutes",
            MutedAccount,
        )
