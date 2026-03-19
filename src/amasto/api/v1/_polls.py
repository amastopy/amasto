from __future__ import annotations

from ..._endpoint import Endpoint, EndpointTemplate
from ...models.v1 import Poll
from typing import TypedDict

__all__ = ("get_polls", "polls")


get_polls: EndpointTemplate[Poll, None, None] = EndpointTemplate(
    "GET",
    "/api/v1/polls/{id}",
    Poll,
    requires="2.8.0",
)


class _VotesBody(TypedDict):
    choices: list[int]


class _PollsById:
    __slots__ = ("post_votes",)

    def __init__(self, id: str, /) -> None:
        self.post_votes: Endpoint[Poll, None, _VotesBody] = Endpoint(
            "POST",
            f"/api/v1/polls/{id}/votes",
            Poll,
            body=_VotesBody,
            requires="2.8.0",
        )


class _PollsNamespace:
    __slots__ = ()

    def __getitem__(self, id: str) -> _PollsById:
        return _PollsById(id)


polls = _PollsNamespace()
