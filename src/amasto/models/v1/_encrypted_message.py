from __future__ import annotations

from amasto._version import since
from pydantic import BaseModel, ConfigDict
from typing import Literal

__all__ = ("EncryptedMessage",)


@since("3.2.0")
class EncryptedMessage(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    account_id: str
    device_id: str
    type: Literal["0", "1"]
    body: str
    digest: str
    message_franking: str
    created_at: str
