from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import CredentialAccount
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("ProfileResource",)


class _AvatarResource:
    __slots__ = ("delete",)

    def __init__(self, client: Amasto, /) -> None:
        self.delete: HttpMethod[CredentialAccount, None, None] = HttpMethod(
            client,
            "DELETE",
            "/api/v1/profile/avatar",
            CredentialAccount,
            requires="4.2.0",
        )


class _HeaderResource:
    __slots__ = ("delete",)

    def __init__(self, client: Amasto, /) -> None:
        self.delete: HttpMethod[CredentialAccount, None, None] = HttpMethod(
            client,
            "DELETE",
            "/api/v1/profile/header",
            CredentialAccount,
            requires="4.2.0",
        )


class ProfileResource:
    __slots__ = ("avatar", "header")

    def __init__(self, client: Amasto, /) -> None:
        self.avatar = _AvatarResource(client)
        self.header = _HeaderResource(client)
