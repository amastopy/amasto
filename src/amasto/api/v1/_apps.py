from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import Application, CredentialApplication
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("AppsResource",)


class _CreateAppBody(TypedDict, total=False):
    client_name: str
    redirect_uris: str
    scopes: str
    website: str


class _VerifyCredentialsResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[Application, None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/apps/verify_credentials",
            Application,
        )


class AppsResource:
    __slots__ = ("post", "verify_credentials")

    def __init__(self, client: Amasto, /) -> None:
        self.post: HttpMethod[CredentialApplication, None, _CreateAppBody] = HttpMethod(
            client,
            "POST",
            "/api/v1/apps",
            CredentialApplication,
        )
        self.verify_credentials = _VerifyCredentialsResource(client)
