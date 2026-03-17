from __future__ import annotations

from amasto._version import since
from pydantic import BaseModel, ConfigDict

__all__ = ("IdentityProof",)


@since("2.8.0")
class IdentityProof(BaseModel):
    model_config = ConfigDict(frozen=True)

    provider: str
    provider_username: str
    updated_at: str
    proof_url: str
    profile_url: str
