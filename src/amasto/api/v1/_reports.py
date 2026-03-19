from __future__ import annotations

from ..._endpoint import Endpoint
from ...models.v1 import Report
from typing import TypedDict

__all__ = ("post_reports",)


class _ReportBody(TypedDict, total=False):
    account_id: str  # required but enforced by the server
    status_ids: list[str]
    comment: str
    forward: bool
    category: str
    rule_ids: list[str]


post_reports: Endpoint[Report, None, _ReportBody] = Endpoint(
    "POST",
    "/api/v1/reports",
    Report,
    body=_ReportBody,
    requires="1.1.0",
)
