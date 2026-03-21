"""amasto — An async-first Python library for the Mastodon API."""

from __future__ import annotations

from . import models
from ._client import Amasto
from typing import Final

__all__: Final = (
    "Amasto",
    "models",
)
