from __future__ import annotations

from amasto._resource import HttpMethod
from unittest.mock import MagicMock
import pytest


@pytest.mark.asyncio
async def test_call_raises_when_not_initialized() -> None:
    client = MagicMock()
    client._initialized = False

    method: HttpMethod[dict, None, None] = HttpMethod(client, "GET", "/test", dict)

    with pytest.raises(RuntimeError, match="Client is not initialized"):
        await method()
