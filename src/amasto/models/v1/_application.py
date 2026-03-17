from __future__ import annotations

from amasto._version import Unsupported, since
from pydantic import BaseModel, ConfigDict

__all__ = ("Application", "CredentialApplication")


class Application(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    website: str | None = None
    id: str | None = None
    redirect_uri: str | None = None
    vapid_key: str | None | Unsupported = since("2.8.0")
    scopes: list[str] | Unsupported = since("4.3.0")
    redirect_uris: list[str] | Unsupported = since("4.3.0")


class CredentialApplication(Application):
    client_id: str
    client_secret: str
    client_secret_expires_at: int | Unsupported = since("4.4.0")
