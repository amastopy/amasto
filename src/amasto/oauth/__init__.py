from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .._client import Amasto

__all__ = ("OAuthNamespace",)


class OAuthNamespace:
    __slots__ = ("authorize", "revoke", "token", "userinfo")

    def __init__(self, client: Amasto, /) -> None:
        from ._authorize import AuthorizeResource
        from ._revoke import RevokeResource
        from ._token import TokenResource
        from ._userinfo import UserinfoResource

        self.authorize = AuthorizeResource(client)
        self.token = TokenResource(client)
        self.revoke = RevokeResource(client)
        self.userinfo = UserinfoResource(client)
