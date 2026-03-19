from __future__ import annotations

from ..._endpoint import Endpoint
from ..._params import PaginationParams
from typing import TypedDict

__all__ = ("delete_domain_blocks", "get_domain_blocks", "post_domain_blocks")


class _DomainBlockBody(TypedDict):
    domain: str


get_domain_blocks: Endpoint[list[str], PaginationParams, None] = Endpoint(
    "GET",
    "/api/v1/domain_blocks",
    list[str],
    params=PaginationParams,
)

post_domain_blocks: Endpoint[dict, None, _DomainBlockBody] = Endpoint(
    "POST",
    "/api/v1/domain_blocks",
    dict,
    body=_DomainBlockBody,
)

delete_domain_blocks: Endpoint[dict, None, _DomainBlockBody] = Endpoint(
    "DELETE",
    "/api/v1/domain_blocks",
    dict,
    body=_DomainBlockBody,
)
