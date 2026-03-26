"""amasto — An async-first Python library for the Mastodon API."""

from __future__ import annotations

from . import models
from ._client import Amasto
from ._streaming import ReconnectPolicy
from ._version import Unsupported
from typing import Final

__all__: Final = (
    "Amasto",
    "ReconnectPolicy",
    "Unsupported",
    "models",
)
