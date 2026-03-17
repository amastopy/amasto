from __future__ import annotations

from pydantic import BaseModel, ConfigDict

__all__ = ("Token",)


class Token(BaseModel):
    model_config = ConfigDict(frozen=True)

    access_token: str
    token_type: str
    scope: str
    created_at: int
