from __future__ import annotations

from ..._endpoint import Endpoint
from ...models.v1 import Account
from typing import TypedDict

__all__ = ("get_directory",)


class _DirectoryParams(TypedDict, total=False):
    offset: int
    limit: int
    order: str
    local: bool


get_directory: Endpoint[list[Account], _DirectoryParams, None] = Endpoint(
    "GET",
    "/api/v1/directory",
    list[Account],
    params=_DirectoryParams,
    requires="3.0.0",
)
