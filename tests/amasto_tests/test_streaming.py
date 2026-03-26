from __future__ import annotations

from amasto._streaming import ReconnectPolicy, _dispatch_event
from amasto.models.v1 import (
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
    UpdateEvent,
)
import json

# ---------------------------------------------------------------------------
# Minimal JSON fixtures
# ---------------------------------------------------------------------------

_ACCOUNT_JSON = {
    "id": "1",
    "username": "alice",
    "acct": "alice",
    "url": None,
    "display_name": "Alice",
    "note": "",
    "avatar": "https://example.com/avatar.png",
    "header": "https://example.com/header.png",
    "locked": False,
    "created_at": "2024-01-01T00:00:00.000Z",
    "statuses_count": 0,
    "followers_count": 0,
    "following_count": 0,
}

_STATUS_JSON = {
    "id": "100",
    "uri": "https://example.com/statuses/100",
    "created_at": "2024-01-01T00:00:00.000Z",
    "account": _ACCOUNT_JSON,
    "content": "<p>Hello</p>",
    "reblogs_count": 0,
    "favourites_count": 0,
    "url": None,
    "in_reply_to_id": None,
    "in_reply_to_account_id": None,
    "reblog": None,
    "media_attachments": [],
    "mentions": [],
    "tags": [],
    "visibility": "public",
    "sensitive": False,
    "application": None,
}

_NOTIFICATION_JSON = {
    "id": "200",
    "type": "favourite",
    "created_at": "2024-01-01T00:00:00.000Z",
    "account": _ACCOUNT_JSON,
}

_CONVERSATION_JSON = {
    "id": "300",
    "unread": False,
    "accounts": [_ACCOUNT_JSON],
    "last_status": None,
}

_ANNOUNCEMENT_JSON = {
    "id": "400",
    "content": "<p>Announcement</p>",
    "starts_at": None,
    "ends_at": None,
    "all_day": False,
    "published_at": "2024-01-01T00:00:00.000Z",
    "updated_at": "2024-01-01T00:00:00.000Z",
    "mentions": [],
    "statuses": [],
    "tags": [],
    "emojis": [],
    "reactions": [],
}

_ENCRYPTED_MESSAGE_JSON = {
    "id": "500",
    "account_id": "1",
    "device_id": "dev1",
    "type": "0",
    "body": "encrypted-body",
    "digest": "abc123",
    "message_franking": "frank",
    "created_at": "2024-01-01T00:00:00.000Z",
}


# ---------------------------------------------------------------------------
# _dispatch_event tests
# ---------------------------------------------------------------------------


def test_dispatch_update() -> None:
    event = _dispatch_event("update", json.dumps(_STATUS_JSON))
    assert isinstance(event, UpdateEvent)
    assert event.status.id == "100"


def test_dispatch_delete() -> None:
    event = _dispatch_event("delete", "12345")
    assert isinstance(event, DeleteEvent)
    assert event.status_id == "12345"


def test_dispatch_notification() -> None:
    event = _dispatch_event("notification", json.dumps(_NOTIFICATION_JSON))
    assert isinstance(event, NotificationEvent)
    assert event.notification.id == "200"


def test_dispatch_filters_changed() -> None:
    event = _dispatch_event("filters_changed", None)
    assert isinstance(event, FiltersChangedEvent)


def test_dispatch_conversation() -> None:
    event = _dispatch_event("conversation", json.dumps(_CONVERSATION_JSON))
    assert isinstance(event, ConversationEvent)
    assert event.conversation.id == "300"


def test_dispatch_announcement() -> None:
    event = _dispatch_event("announcement", json.dumps(_ANNOUNCEMENT_JSON))
    assert isinstance(event, AnnouncementEvent)
    assert event.announcement.id == "400"


def test_dispatch_announcement_reaction() -> None:
    payload = json.dumps({"name": "👍", "count": 3, "announcement_id": "400"})
    event = _dispatch_event("announcement.reaction", payload)
    assert isinstance(event, AnnouncementReactionEvent)
    assert event.name == "👍"
    assert event.count == 3
    assert event.announcement_id == "400"


def test_dispatch_announcement_delete() -> None:
    event = _dispatch_event("announcement.delete", "400")
    assert isinstance(event, AnnouncementDeleteEvent)
    assert event.announcement_id == "400"


def test_dispatch_status_update() -> None:
    event = _dispatch_event("status.update", json.dumps(_STATUS_JSON))
    assert isinstance(event, StatusUpdateEvent)
    assert event.status.id == "100"


def test_dispatch_encrypted_message() -> None:
    event = _dispatch_event("encrypted_message", json.dumps(_ENCRYPTED_MESSAGE_JSON))
    assert isinstance(event, EncryptedMessageEvent)
    assert event.encrypted_message.id == "500"


def test_dispatch_notifications_merged() -> None:
    event = _dispatch_event("notifications_merged", None)
    assert isinstance(event, NotificationsMergedEvent)


def test_dispatch_unknown_event_returns_none() -> None:
    assert _dispatch_event("unknown.future.event", "{}") is None


# ---------------------------------------------------------------------------
# ReconnectPolicy tests
# ---------------------------------------------------------------------------


def test_reconnect_policy_defaults() -> None:
    p = ReconnectPolicy()
    assert p.max_retries is None
    assert p.initial_delay == 1.0
    assert p.max_delay == 30.0
    assert p.multiplier == 2.0


def test_reconnect_policy_custom() -> None:
    p = ReconnectPolicy(max_retries=5, initial_delay=0.5, max_delay=10.0, multiplier=3.0)
    assert p.max_retries == 5
    assert p.initial_delay == 0.5
    assert p.max_delay == 10.0
    assert p.multiplier == 3.0
