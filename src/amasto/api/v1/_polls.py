from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import Poll
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("PollsResource",)


class _VotesBody(TypedDict):
    choices: list[int]


class _VotesResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Poll, None, _VotesBody] = HttpMethod(
            client,
            "POST",
            f"/api/v1/polls/{id}/votes",
            Poll,
            requires="2.8.0",
        )


class _PollByIdResource:
    __slots__ = ("get", "votes")

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[Poll, None, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/polls/{id}",
            Poll,
            requires="2.8.0",
        )
        self.votes = _VotesResource(client, id)


class PollsResource:
    __slots__ = ("_client",)

    def __init__(self, client: Amasto, /) -> None:
        self._client = client

    def __getitem__(self, id: str) -> _PollByIdResource:
        return _PollByIdResource(self._client, id)
