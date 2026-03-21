from __future__ import annotations

from .._resource import HttpMethod
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from .._client import Amasto

__all__ = ("AuthorizeResource",)


class _AuthorizeParams(TypedDict, total=False):
    response_type: str
    client_id: str
    redirect_uri: str
    scope: str
    state: str
    code_challenge: str
    code_challenge_method: str
    force_login: bool
    lang: str


class AuthorizeResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[dict, _AuthorizeParams, None] = HttpMethod(
            client,
            "GET",
            "/oauth/authorize",
            dict,
        )
