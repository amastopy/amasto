from __future__ import annotations

from ..._endpoint import Endpoint
from ...models.v1 import Application, CredentialApplication
from typing import TypedDict

__all__ = ("apps", "post_apps")


class _CreateAppBody(TypedDict, total=False):
    client_name: str
    redirect_uris: str
    scopes: str
    website: str


post_apps: Endpoint[CredentialApplication, None, _CreateAppBody] = Endpoint(
    "POST",
    "/api/v1/apps",
    CredentialApplication,
    body=_CreateAppBody,
)


class _AppsNamespace:
    __slots__ = ()

    get_verify_credentials = Endpoint("GET", "/api/v1/apps/verify_credentials", Application)


apps = _AppsNamespace()
