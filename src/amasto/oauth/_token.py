from __future__ import annotations

from .._endpoint import Endpoint
from ..models.v1 import Token
from typing import TypedDict

__all__ = ("post_token",)


class _TokenBody(TypedDict, total=False):
    grant_type: str
    code: str
    client_id: str
    client_secret: str
    redirect_uri: str
    code_verifier: str
    scope: str


post_token: Endpoint[Token, None, _TokenBody] = Endpoint(
    "POST", "/oauth/token", Token, body=_TokenBody,
)
