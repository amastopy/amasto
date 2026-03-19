from __future__ import annotations

from ..._endpoint import Endpoint, EndpointTemplate, SubscriptableEndpoint
from ..._params import PaginationParams
from ...models.v1 import Account, Context, Status, StatusEdit, StatusSource, Translation
from typing import TypedDict

__all__ = ("delete_statuses", "get_statuses", "post_statuses", "put_statuses", "statuses")


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
    visibility: str
    language: str
    scheduled_at: str
    quoted_status_id: str
    quote_approval_policy: str


class _EditStatusBody(TypedDict, total=False):
    status: str
    spoiler_text: str
    sensitive: bool
    language: str
    media_ids: list[str]
    poll: _CreateStatusPoll
    quote_approval_policy: str


class _DeleteStatusParams(TypedDict, total=False):
    delete_media: bool


class _TranslateBody(TypedDict, total=False):
    lang: str


class _ReblogBody(TypedDict, total=False):
    visibility: str


class _InteractionPolicyBody(TypedDict, total=False):
    quote_approval_policy: str


# ---------------------------------------------------------------------------
# Flat endpoints
# ---------------------------------------------------------------------------


post_statuses: Endpoint[Status, None, _CreateStatusBody] = Endpoint(
    "POST",
    "/api/v1/statuses",
    Status,
    body=_CreateStatusBody,
)

get_statuses: SubscriptableEndpoint[list[Status], _GetStatusesParams, None, Status] = SubscriptableEndpoint(
    "GET",
    "/api/v1/statuses",
    list[Status],
    "/api/v1/statuses/{id}",
    Status,
    params=_GetStatusesParams,
    requires="4.3.0",
)

delete_statuses: EndpointTemplate[Status, _DeleteStatusParams, None] = EndpointTemplate(
    "DELETE",
    "/api/v1/statuses/{id}",
    Status,
    params=_DeleteStatusParams,
)

put_statuses: EndpointTemplate[Status, None, _EditStatusBody] = EndpointTemplate(
    "PUT",
    "/api/v1/statuses/{id}",
    Status,
    body=_EditStatusBody,
    requires="3.5.0",
)


# ---------------------------------------------------------------------------
# By-ID namespace
# ---------------------------------------------------------------------------


class _StatusQuotesById:
    __slots__ = ("post_revoke",)

    def __init__(self, status_id: str, quoting_status_id: str, /) -> None:
        self.post_revoke = Endpoint(
            "POST",
            f"/api/v1/statuses/{status_id}/quotes/{quoting_status_id}/revoke",
            Status,
            requires="4.5.0",
        )


class _StatusQuotesNamespace:
    __slots__ = ("_status_id", "get_quotes")

    def __init__(self, status_id: str, /) -> None:
        self._status_id = status_id
        self.get_quotes: Endpoint[list[Status], PaginationParams, None] = Endpoint(
            "GET",
            f"/api/v1/statuses/{status_id}/quotes",
            list[Status],
            params=PaginationParams,
            requires="4.5.0",
        )

    def __getitem__(self, quoting_status_id: str) -> _StatusQuotesById:
        return _StatusQuotesById(self._status_id, quoting_status_id)


class _StatusesById:
    __slots__ = (
        "get_context",
        "get_favourited_by",
        "get_history",
        "get_reblogged_by",
        "get_source",
        "post_bookmark",
        "post_favourite",
        "post_mute",
        "post_pin",
        "post_reblog",
        "post_translate",
        "post_unbookmark",
        "post_unfavourite",
        "post_unmute",
        "post_unpin",
        "post_unreblog",
        "put_interaction_policy",
        "quotes",
    )

    def __init__(self, id: str, /) -> None:
        p = f"/api/v1/statuses/{id}"

        self.get_context = Endpoint("GET", f"{p}/context", Context)
        self.post_translate: Endpoint[Translation, None, _TranslateBody] = Endpoint(
            "POST",
            f"{p}/translate",
            Translation,
            body=_TranslateBody,
            requires="4.0.0",
        )
        self.get_reblogged_by: Endpoint[list[Account], PaginationParams, None] = Endpoint(
            "GET",
            f"{p}/reblogged_by",
            list[Account],
            params=PaginationParams,
        )
        self.get_favourited_by: Endpoint[list[Account], PaginationParams, None] = Endpoint(
            "GET",
            f"{p}/favourited_by",
            list[Account],
            params=PaginationParams,
        )
        self.get_history: Endpoint[list[StatusEdit], None, None] = Endpoint(
            "GET",
            f"{p}/history",
            list[StatusEdit],
            requires="3.5.0",
        )
        self.get_source = Endpoint("GET", f"{p}/source", StatusSource, requires="3.5.0")

        self.post_favourite = Endpoint("POST", f"{p}/favourite", Status)
        self.post_unfavourite = Endpoint("POST", f"{p}/unfavourite", Status)
        self.post_reblog: Endpoint[Status, None, _ReblogBody] = Endpoint(
            "POST",
            f"{p}/reblog",
            Status,
            body=_ReblogBody,
        )
        self.post_unreblog = Endpoint("POST", f"{p}/unreblog", Status)
        self.post_bookmark = Endpoint("POST", f"{p}/bookmark", Status, requires="3.1.0")
        self.post_unbookmark = Endpoint("POST", f"{p}/unbookmark", Status, requires="3.1.0")
        self.post_mute = Endpoint("POST", f"{p}/mute", Status, requires="1.4.2")
        self.post_unmute = Endpoint("POST", f"{p}/unmute", Status, requires="1.4.2")
        self.post_pin = Endpoint("POST", f"{p}/pin", Status, requires="1.6.0")
        self.post_unpin = Endpoint("POST", f"{p}/unpin", Status, requires="1.6.0")
        self.put_interaction_policy: Endpoint[Status, None, _InteractionPolicyBody] = Endpoint(
            "PUT",
            f"{p}/interaction_policy",
            Status,
            body=_InteractionPolicyBody,
            requires="4.5.0",
        )

        self.quotes = _StatusQuotesNamespace(id)


# ---------------------------------------------------------------------------
# Namespace
# ---------------------------------------------------------------------------


class _StatusesNamespace:
    __slots__ = ()

    def __getitem__(self, id: str) -> _StatusesById:
        return _StatusesById(id)


statuses = _StatusesNamespace()
