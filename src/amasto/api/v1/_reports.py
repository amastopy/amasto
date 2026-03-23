from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import Report
from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("ReportsResource",)


class _ReportBody(TypedDict, total=False):
    account_id: str  # required but enforced by the server
    status_ids: list[str]
    comment: str
    forward: bool
    category: str | Literal["spam", "legal", "violation", "other"]
    rule_ids: list[str]


class ReportsResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, /) -> None:
        self.post: HttpMethod[Report, None, _ReportBody] = HttpMethod(
            client,
            "POST",
            "/api/v1/reports",
            Report,
            requires="1.1.0",
        )
