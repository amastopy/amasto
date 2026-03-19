from __future__ import annotations

from ..._endpoint import Endpoint
from typing import TypedDict

__all__ = ("emails",)


class _ConfirmationBody(TypedDict, total=False):
    email: str


class _EmailsNamespace:
    __slots__ = ()

    post_confirmations: Endpoint[dict, None, _ConfirmationBody] = Endpoint(
        "POST",
        "/api/v1/emails/confirmations",
        dict,
        body=_ConfirmationBody,
        requires="2.7.2",
    )


emails = _EmailsNamespace()
