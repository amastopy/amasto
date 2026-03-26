from __future__ import annotations

from ._announcement import Announcement
from ._conversation import Conversation
from ._encrypted_message import EncryptedMessage
from ._notification import Notification
from ._status import Status
from pydantic import BaseModel, ConfigDict

__all__ = (
    "AnnouncementDeleteEvent",
    "AnnouncementEvent",
    "AnnouncementReactionEvent",
    "ConversationEvent",
    "DeleteEvent",
    "EncryptedMessageEvent",
    "FiltersChangedEvent",
    "NotificationEvent",
    "NotificationsMergedEvent",
    "StatusUpdateEvent",
    "StreamEvent",
    "UpdateEvent",
)


class UpdateEvent(BaseModel):
    """``event: update`` — A new Status has appeared."""

    model_config = ConfigDict(frozen=True)

    status: Status


class DeleteEvent(BaseModel):
    """``event: delete`` — A status has been deleted."""

    model_config = ConfigDict(frozen=True)

    status_id: str


class NotificationEvent(BaseModel):
    """``event: notification`` — A new notification has appeared."""

    model_config = ConfigDict(frozen=True)

    notification: Notification


class FiltersChangedEvent(BaseModel):
    """``event: filters_changed`` — Keyword filters have been changed."""

    model_config = ConfigDict(frozen=True)


class ConversationEvent(BaseModel):
    """``event: conversation`` — A direct conversation has been updated."""

    model_config = ConfigDict(frozen=True)

    conversation: Conversation


class AnnouncementEvent(BaseModel):
    """``event: announcement`` — An announcement has been published."""

    model_config = ConfigDict(frozen=True)

    announcement: Announcement


class AnnouncementReactionEvent(BaseModel):
    """``event: announcement.reaction`` — An announcement has received an emoji reaction."""

    model_config = ConfigDict(frozen=True)

    name: str
    count: int
    announcement_id: str


class AnnouncementDeleteEvent(BaseModel):
    """``event: announcement.delete`` — An announcement has been deleted."""

    model_config = ConfigDict(frozen=True)

    announcement_id: str


class StatusUpdateEvent(BaseModel):
    """``event: status.update`` — A Status has been edited."""

    model_config = ConfigDict(frozen=True)

    status: Status


class EncryptedMessageEvent(BaseModel):
    """``event: encrypted_message`` — An encrypted message has been received."""

    model_config = ConfigDict(frozen=True)

    encrypted_message: EncryptedMessage


class NotificationsMergedEvent(BaseModel):
    """``event: notifications_merged`` — Notification requests have finished merging."""

    model_config = ConfigDict(frozen=True)


type StreamEvent = (
    UpdateEvent
    | DeleteEvent
    | NotificationEvent
    | FiltersChangedEvent
    | ConversationEvent
    | AnnouncementEvent
    | AnnouncementReactionEvent
    | AnnouncementDeleteEvent
    | StatusUpdateEvent
    | EncryptedMessageEvent
    | NotificationsMergedEvent
)
