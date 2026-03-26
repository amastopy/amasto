from __future__ import annotations

from ..._pagination import PaginatedHttpMethod
from ..._params import PaginationParams
from ..._resource import HttpMethod
from ...models.v1 import Conversation
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("ConversationsResource",)


class _ReadResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Conversation, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/conversations/{id}/read",
            Conversation,
            requires="2.6.0",
        )


class _ConversationByIdResource:
    __slots__ = ("delete", "read")

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.delete: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "DELETE",
            f"/api/v1/conversations/{id}",
            dict,
            requires="2.6.0",
        )
        self.read = _ReadResource(client, id)


class ConversationsResource:
    __slots__ = ("_client", "get")

    def __init__(self, client: Amasto, /) -> None:
        self._client = client
        self.get: PaginatedHttpMethod[Conversation, PaginationParams] = PaginatedHttpMethod(
            client,
            "GET",
            "/api/v1/conversations",
            Conversation,
            requires="2.6.0",
        )

    def __getitem__(self, id: str) -> _ConversationByIdResource:
        return _ConversationByIdResource(self._client, id)
