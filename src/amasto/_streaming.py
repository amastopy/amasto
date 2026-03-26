from __future__ import annotations

from .models.v1._stream_event import (
    AnnouncementDeleteEvent,
    AnnouncementEvent,
    AnnouncementReactionEvent,
    ConversationEvent,
    DeleteEvent,
    EncryptedMessageEvent,
    FiltersChangedEvent,
    NotificationEvent,
    NotificationsMergedEvent,
    StatusUpdateEvent,
    StreamEvent,
    UpdateEvent,
)
import asyncio
from dataclasses import dataclass
import json
import logging
from typing import TYPE_CHECKING
import websockets

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

__all__ = ("ReconnectPolicy", "stream_events")

_log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ReconnectPolicy:
    """Configuration for automatic reconnection with exponential back-off."""

    max_retries: int | None = None
    """Maximum number of reconnection attempts. ``None`` means unlimited."""

    initial_delay: float = 1.0
    """Seconds to wait before the first reconnection attempt."""

    max_delay: float = 30.0
    """Upper-bound on the delay between reconnection attempts."""

    multiplier: float = 2.0
    """Factor by which the delay increases after each failed attempt."""


_DEFAULT_RECONNECT = ReconnectPolicy()


def _dispatch_event(event: str, payload: str | None) -> StreamEvent | None:
    """Convert a raw WebSocket event name + payload into a typed model."""
    match event:
        case "update":
            from .models.v1 import Status as _Status

            return UpdateEvent(status=_Status.model_validate_json(payload))  # type: ignore[arg-type]
        case "delete":
            return DeleteEvent(status_id=payload or "")
        case "notification":
            from .models.v1 import Notification as _Notification

            return NotificationEvent(notification=_Notification.model_validate_json(payload))  # type: ignore[arg-type]
        case "filters_changed":
            return FiltersChangedEvent()
        case "conversation":
            from .models.v1 import Conversation as _Conversation

            return ConversationEvent(conversation=_Conversation.model_validate_json(payload))  # type: ignore[arg-type]
        case "announcement":
            from .models.v1 import Announcement as _Announcement

            return AnnouncementEvent(announcement=_Announcement.model_validate_json(payload))  # type: ignore[arg-type]
        case "announcement.reaction":
            return AnnouncementReactionEvent.model_validate_json(payload)  # type: ignore[arg-type]
        case "announcement.delete":
            return AnnouncementDeleteEvent(announcement_id=payload or "")
        case "status.update":
            from .models.v1 import Status as _Status

            return StatusUpdateEvent(status=_Status.model_validate_json(payload))  # type: ignore[arg-type]
        case "encrypted_message":
            from .models.v1 import EncryptedMessage as _EncryptedMessage

            return EncryptedMessageEvent(encrypted_message=_EncryptedMessage.model_validate_json(payload))  # type: ignore[arg-type]
        case "notifications_merged":
            return NotificationsMergedEvent()
        case _:
            _log.debug("Ignoring unknown streaming event: %s", event)
            return None


async def stream_events(
    streaming_url: str,
    api_key: str,
    stream: str,
    *,
    params: dict[str, str] | None = None,
    reconnect: ReconnectPolicy | None = None,
) -> AsyncIterator[StreamEvent]:
    """Open a WebSocket connection and yield typed streaming events.

    Parameters
    ----------
    streaming_url
        Base URL of the streaming server (``https://...``).  The scheme is
        automatically converted to ``wss://`` for the WebSocket handshake.
    api_key
        Bearer token for authentication.
    stream
        Stream name to subscribe to (e.g. ``"user"``, ``"public"``).
    params
        Additional subscription parameters (``tag``, ``list``, …).
    reconnect
        Reconnection policy.  Pass ``None`` to use the default policy.
    """
    policy = reconnect if reconnect is not None else _DEFAULT_RECONNECT

    ws_url = f"{streaming_url}/api/v1/streaming"

    subscribe_payload: dict[str, str] = {"type": "subscribe", "stream": stream}
    if params:
        subscribe_payload.update(params)

    attempts = 0
    delay = policy.initial_delay

    while True:
        try:
            async with websockets.connect(
                ws_url,
                additional_headers={"Authorization": f"Bearer {api_key}"},
            ) as ws:
                # Reset back-off on successful connection.
                attempts = 0
                delay = policy.initial_delay

                await ws.send(json.dumps(subscribe_payload))

                async for raw_message in ws:
                    if isinstance(raw_message, bytes):
                        raw_message = raw_message.decode()

                    try:
                        message = json.loads(raw_message)
                    except json.JSONDecodeError:
                        _log.debug("Ignoring non-JSON WebSocket message")
                        continue

                    event_name: str | None = message.get("event")
                    if event_name is None:
                        continue

                    payload: str | None = message.get("payload")

                    dispatched = _dispatch_event(event_name, payload)
                    if dispatched is not None:
                        yield dispatched

        except websockets.exceptions.InvalidStatus as exc:
            # 4xx handshake failures should not be retried.
            if exc.response is not None and 400 <= exc.response.status_code < 500:
                raise
            # 5xx — fall through to reconnect logic.
            status = exc.response.status_code if exc.response else "unknown"
            _log.warning("WebSocket handshake failed (status %s), reconnecting…", status)
        except (
            websockets.exceptions.ConnectionClosedError,
            websockets.exceptions.ConnectionClosedOK,
            OSError,
        ):
            _log.info("WebSocket connection lost, reconnecting…")

        # Reconnect with exponential back-off.
        attempts += 1
        if policy.max_retries is not None and attempts > policy.max_retries:
            raise ConnectionError(f"Failed to reconnect after {policy.max_retries} attempts")

        _log.debug("Reconnecting in %.1fs (attempt %d)", delay, attempts)
        await asyncio.sleep(delay)
        delay = min(delay * policy.multiplier, policy.max_delay)
