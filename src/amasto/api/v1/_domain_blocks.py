from __future__ import annotations

from ..._params import PaginationParams
from ..._resource import HttpMethod
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("DomainBlocksResource",)


class _DomainBlockBody(TypedDict):
    domain: str


class DomainBlocksResource:
    __slots__ = ("delete", "get", "post")

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[str], PaginationParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/domain_blocks",
            list[str],
        )
        self.post: HttpMethod[dict, None, _DomainBlockBody] = HttpMethod(
            client,
            "POST",
            "/api/v1/domain_blocks",
            dict,
        )
        self.delete: HttpMethod[dict, None, _DomainBlockBody] = HttpMethod(
            client,
            "DELETE",
            "/api/v1/domain_blocks",
            dict,
        )
