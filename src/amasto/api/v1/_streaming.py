from __future__ import annotations

from ..._streaming import ReconnectPolicy, stream_events
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto
    from ...models.v1 import StreamEvent
    from collections.abc import AsyncIterator

__all__ = ("StreamingResource",)


class StreamingResource:
    __slots__ = ("_client",)

    def __init__(self, client: Amasto, /) -> None:
        self._client = client

    def _stream(
        self,
        stream: str,
        *,
        params: dict[str, str] | None = None,
        reconnect: ReconnectPolicy | None = None,
    ) -> AsyncIterator[StreamEvent]:
        return stream_events(
            self._client._streaming_url,  # noqa: SLF001
            self._client._api_key,  # noqa: SLF001
            stream,
            params=params,
            reconnect=reconnect,
        )

    async def user(
        self,
        *,
        reconnect: ReconnectPolicy | None = None,
    ) -> AsyncIterator[StreamEvent]:
        async for event in self._stream("user", reconnect=reconnect):
            yield event

    async def user_notification(
        self,
        *,
        reconnect: ReconnectPolicy | None = None,
    ) -> AsyncIterator[StreamEvent]:
        async for event in self._stream("user:notification", reconnect=reconnect):
            yield event

    async def public(
        self,
        *,
        only_media: bool = False,
        reconnect: ReconnectPolicy | None = None,
    ) -> AsyncIterator[StreamEvent]:
        stream = "public:media" if only_media else "public"
        async for event in self._stream(stream, reconnect=reconnect):
            yield event

    async def public_local(
        self,
        *,
        only_media: bool = False,
        reconnect: ReconnectPolicy | None = None,
    ) -> AsyncIterator[StreamEvent]:
        stream = "public:local:media" if only_media else "public:local"
        async for event in self._stream(stream, reconnect=reconnect):
            yield event

    async def public_remote(
        self,
        *,
        only_media: bool = False,
        reconnect: ReconnectPolicy | None = None,
    ) -> AsyncIterator[StreamEvent]:
        stream = "public:remote:media" if only_media else "public:remote"
        async for event in self._stream(stream, reconnect=reconnect):
            yield event

    async def hashtag(
        self,
        tag: str,
        *,
        local: bool = False,
        reconnect: ReconnectPolicy | None = None,
    ) -> AsyncIterator[StreamEvent]:
        stream = "hashtag:local" if local else "hashtag"
        async for event in self._stream(stream, params={"tag": tag}, reconnect=reconnect):
            yield event

    async def list(
        self,
        list_id: str,
        *,
        reconnect: ReconnectPolicy | None = None,
    ) -> AsyncIterator[StreamEvent]:
        async for event in self._stream("list", params={"list": list_id}, reconnect=reconnect):
            yield event

    async def direct(
        self,
        *,
        reconnect: ReconnectPolicy | None = None,
    ) -> AsyncIterator[StreamEvent]:
        async for event in self._stream("direct", reconnect=reconnect):
            yield event
