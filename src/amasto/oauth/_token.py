from __future__ import annotations

from .._resource import HttpMethod
from ..models.v1 import Token
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from .._client import Amasto

__all__ = ("TokenResource",)


class _TokenBody(TypedDict, total=False):
    grant_type: str
    code: str
    client_id: str
    client_secret: str
    redirect_uri: str
    code_verifier: str
    scope: str


class TokenResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, /) -> None:
        self.post: HttpMethod[Token, None, _TokenBody] = HttpMethod(
            client,
            "POST",
            "/oauth/token",
            Token,
        )
