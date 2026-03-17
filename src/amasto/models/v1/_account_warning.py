from __future__ import annotations

from ._account import Account
from ._appeal import Appeal
from amasto._version import since
from pydantic import BaseModel, ConfigDict
from typing import Literal

__all__ = ("AccountWarning",)


@since("4.3.0")
class AccountWarning(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    action: Literal[
        "none",
        "disable",
        "mark_statuses_as_sensitive",
        "delete_statuses",
        "sensitive",
        "silence",
        "suspend",
    ]
    text: str
    status_ids: list[str] | None
    target_account: Account
    appeal: Appeal | None
    created_at: str
