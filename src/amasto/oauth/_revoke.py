from __future__ import annotations

from .._endpoint import Endpoint
from typing import TypedDict

__all__ = ("post_revoke",)


class _RevokeBody(TypedDict, total=False):
    client_id: str
    client_secret: str
    token: str


post_revoke: Endpoint[dict, None, _RevokeBody] = Endpoint(
    "POST",
    "/oauth/revoke",
    dict,
    body=_RevokeBody,
    requires="1.5.0",
)
