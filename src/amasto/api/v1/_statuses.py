from __future__ import annotations

from ..._params import PaginationParams
from ..._resource import HttpMethod
from ...models.v1 import Account, Context, Status, StatusEdit, StatusSource, Translation
from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("StatusesResource",)


# ---------------------------------------------------------------------------
# TypedDicts
# ---------------------------------------------------------------------------


class _GetStatusesParams(TypedDict):
    id: list[str]


class _CreateStatusPoll(TypedDict, total=False):
    options: list[str]
    expires_in: int
    multiple: bool
    hide_totals: bool


class _CreateStatusBody(TypedDict, total=False):
    status: str
    media_ids: list[str]
    poll: _CreateStatusPoll
    in_reply_to_id: str
    sensitive: bool
    spoiler_text: str
    visibility: str | Literal["public", "unlisted", "private", "direct"]
    language: str
    scheduled_at: str
    quoted_status_id: str
    quote_approval_policy: str | Literal["public", "followers", "nobody"]


class _EditStatusBody(TypedDict, total=False):
    status: str
    spoiler_text: str
    sensitive: bool
    language: str
    media_ids: list[str]
    poll: _CreateStatusPoll
    quote_approval_policy: str | Literal["public", "followers", "nobody"]


class _DeleteStatusParams(TypedDict, total=False):
    delete_media: bool


class _TranslateBody(TypedDict, total=False):
    lang: str


class _ReblogBody(TypedDict, total=False):
    visibility: str | Literal["public", "unlisted", "private"]


class _InteractionPolicyBody(TypedDict, total=False):
    quote_approval_policy: str | Literal["public", "followers", "nobody"]


# ---------------------------------------------------------------------------
# Sub-resources for by-ID
# ---------------------------------------------------------------------------


class _ContextResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[Context, None, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/statuses/{id}/context",
            Context,
        )


class _TranslateResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Translation, None, _TranslateBody] = HttpMethod(
            client,
            "POST",
            f"/api/v1/statuses/{id}/translate",
            Translation,
            requires="4.0.0",
        )


class _RebloggedByResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[list[Account], PaginationParams, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/statuses/{id}/reblogged_by",
            list[Account],
        )


class _FavouritedByResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[list[Account], PaginationParams, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/statuses/{id}/favourited_by",
            list[Account],
        )


class _HistoryResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[list[StatusEdit], None, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/statuses/{id}/history",
            list[StatusEdit],
            requires="3.5.0",
        )


class _SourceResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[StatusSource, None, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/statuses/{id}/source",
            StatusSource,
            requires="3.5.0",
        )


class _FavouriteActionResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Status, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/statuses/{id}/favourite",
            Status,
        )


class _UnfavouriteResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Status, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/statuses/{id}/unfavourite",
            Status,
        )


class _ReblogActionResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Status, None, _ReblogBody] = HttpMethod(
            client,
            "POST",
            f"/api/v1/statuses/{id}/reblog",
            Status,
        )


class _UnreblogResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Status, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/statuses/{id}/unreblog",
            Status,
        )


class _BookmarkActionResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Status, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/statuses/{id}/bookmark",
            Status,
            requires="3.1.0",
        )


class _UnbookmarkResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Status, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/statuses/{id}/unbookmark",
            Status,
            requires="3.1.0",
        )


class _MuteStatusResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Status, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/statuses/{id}/mute",
            Status,
            requires="1.4.2",
        )


class _UnmuteStatusResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Status, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/statuses/{id}/unmute",
            Status,
            requires="1.4.2",
        )


class _PinStatusResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Status, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/statuses/{id}/pin",
            Status,
            requires="1.6.0",
        )


class _UnpinStatusResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Status, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/statuses/{id}/unpin",
            Status,
            requires="1.6.0",
        )


class _InteractionPolicyResource:
    __slots__ = ("put",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.put: HttpMethod[Status, None, _InteractionPolicyBody] = HttpMethod(
            client,
            "PUT",
            f"/api/v1/statuses/{id}/interaction_policy",
            Status,
            requires="4.5.0",
        )


class _RevokeResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, status_id: str, quoting_id: str, /) -> None:
        self.post: HttpMethod[Status, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/statuses/{status_id}/quotes/{quoting_id}/revoke",
            Status,
            requires="4.5.0",
        )


class _QuoteByIdResource:
    __slots__ = ("revoke",)

    def __init__(self, client: Amasto, status_id: str, quoting_id: str, /) -> None:
        self.revoke = _RevokeResource(client, status_id, quoting_id)


class _QuotesResource:
    __slots__ = ("_client", "_status_id", "get")

    def __init__(self, client: Amasto, status_id: str, /) -> None:
        self._client = client
        self._status_id = status_id
        self.get: HttpMethod[list[Status], PaginationParams, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/statuses/{status_id}/quotes",
            list[Status],
            requires="4.5.0",
        )

    def __getitem__(self, quoting_id: str) -> _QuoteByIdResource:
        return _QuoteByIdResource(self._client, self._status_id, quoting_id)


# ---------------------------------------------------------------------------
# By-ID resource
# ---------------------------------------------------------------------------


class _StatusByIdResource:
    __slots__ = (
        "bookmark",
        "context",
        "delete",
        "favourite",
        "favourited_by",
        "get",
        "history",
        "interaction_policy",
        "mute",
        "pin",
        "put",
        "quotes",
        "reblog",
        "reblogged_by",
        "source",
        "translate",
        "unbookmark",
        "unfavourite",
        "unmute",
        "unpin",
        "unreblog",
    )

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[Status, None, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/statuses/{id}",
            Status,
        )
        self.put: HttpMethod[Status, None, _EditStatusBody] = HttpMethod(
            client,
            "PUT",
            f"/api/v1/statuses/{id}",
            Status,
            requires="3.5.0",
        )
        self.delete: HttpMethod[Status, _DeleteStatusParams, None] = HttpMethod(
            client,
            "DELETE",
            f"/api/v1/statuses/{id}",
            Status,
        )
        self.context = _ContextResource(client, id)
        self.translate = _TranslateResource(client, id)
        self.reblogged_by = _RebloggedByResource(client, id)
        self.favourited_by = _FavouritedByResource(client, id)
        self.history = _HistoryResource(client, id)
        self.source = _SourceResource(client, id)
        self.favourite = _FavouriteActionResource(client, id)
        self.unfavourite = _UnfavouriteResource(client, id)
        self.reblog = _ReblogActionResource(client, id)
        self.unreblog = _UnreblogResource(client, id)
        self.bookmark = _BookmarkActionResource(client, id)
        self.unbookmark = _UnbookmarkResource(client, id)
        self.mute = _MuteStatusResource(client, id)
        self.unmute = _UnmuteStatusResource(client, id)
        self.pin = _PinStatusResource(client, id)
        self.unpin = _UnpinStatusResource(client, id)
        self.interaction_policy = _InteractionPolicyResource(client, id)
        self.quotes = _QuotesResource(client, id)


# ---------------------------------------------------------------------------
# Top-level resource
# ---------------------------------------------------------------------------


class StatusesResource:
    __slots__ = ("_client", "get", "post")

    def __init__(self, client: Amasto, /) -> None:
        self._client = client
        self.get: HttpMethod[list[Status], _GetStatusesParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/statuses",
            list[Status],
            requires="4.3.0",
        )
        self.post: HttpMethod[Status, None, _CreateStatusBody] = HttpMethod(
            client,
            "POST",
            "/api/v1/statuses",
            Status,
        )

    def __getitem__(self, id: str) -> _StatusByIdResource:
        return _StatusByIdResource(self._client, id)
