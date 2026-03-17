from __future__ import annotations

from amasto._version import since
from pydantic import BaseModel, ConfigDict
from typing import Literal

__all__ = ("RelationshipSeveranceEvent",)


@since("4.3.0")
class RelationshipSeveranceEvent(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    type: Literal["domain_block", "user_domain_block", "account_suspension"]
    purged: bool
    target_name: str
    followers_count: int
    following_count: int
    created_at: str
