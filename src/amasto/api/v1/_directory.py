from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import Account
from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("DirectoryResource",)


class _DirectoryParams(TypedDict, total=False):
    offset: int
    limit: int
    order: str | Literal["active", "new"]
    local: bool


class DirectoryResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[Account], _DirectoryParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/directory",
            list[Account],
            requires="3.0.0",
        )
