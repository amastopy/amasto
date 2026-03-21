from __future__ import annotations

from ..._resource import HttpMethod
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("EmailsResource",)


class _ConfirmationBody(TypedDict, total=False):
    email: str


class _ConfirmationsResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, /) -> None:
        self.post: HttpMethod[dict, None, _ConfirmationBody] = HttpMethod(
            client,
            "POST",
            "/api/v1/emails/confirmations",
            dict,
            requires="2.7.2",
        )


class EmailsResource:
    __slots__ = ("confirmations",)

    def __init__(self, client: Amasto, /) -> None:
        self.confirmations = _ConfirmationsResource(client)
