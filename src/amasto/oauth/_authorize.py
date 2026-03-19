from __future__ import annotations

from .._endpoint import Endpoint
from typing import TypedDict

__all__ = ("get_authorize",)


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


get_authorize: Endpoint[dict, _AuthorizeParams, None] = Endpoint(
    "GET", "/oauth/authorize", dict, params=_AuthorizeParams,
)
