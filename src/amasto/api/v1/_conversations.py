from __future__ import annotations

from ..._endpoint import Endpoint, EndpointTemplate
from ..._params import PaginationParams
from ...models.v1 import Conversation

__all__ = ("conversations", "delete_conversations", "get_conversations")


get_conversations: Endpoint[list[Conversation], PaginationParams, None] = Endpoint(
    "GET",
    "/api/v1/conversations",
    list[Conversation],
    params=PaginationParams,
    requires="2.6.0",
)

delete_conversations: EndpointTemplate[dict, None, None] = EndpointTemplate(
    "DELETE",
    "/api/v1/conversations/{id}",
    dict,
    requires="2.6.0",
)


class _ConversationsById:
    __slots__ = ("post_read",)

    def __init__(self, id: str, /) -> None:
        self.post_read = Endpoint("POST", f"/api/v1/conversations/{id}/read", Conversation, requires="2.6.0")


class _ConversationsNamespace:
    __slots__ = ()

    def __getitem__(self, id: str) -> _ConversationsById:
        return _ConversationsById(id)


conversations = _ConversationsNamespace()
