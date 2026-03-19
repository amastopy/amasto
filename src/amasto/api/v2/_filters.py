from __future__ import annotations

from ..._endpoint import Endpoint, EndpointTemplate, SubscriptableEndpoint
from ...models.v2 import Filter, FilterKeyword, FilterStatus
from typing import TypedDict

__all__ = ("delete_filters", "filters", "get_filters", "post_filters", "put_filters")


# ---------------------------------------------------------------------------
# TypedDicts
# ---------------------------------------------------------------------------


class _CreateFilterBody(TypedDict, total=False):
    title: str
    context: list[str]
    filter_action: str
    expires_in: int


class _UpdateFilterBody(TypedDict, total=False):
    title: str
    context: list[str]
    filter_action: str
    expires_in: int


class _CreateKeywordBody(TypedDict, total=False):
    keyword: str
    whole_word: bool


class _CreateFilterStatusBody(TypedDict):
    status_id: str


# ---------------------------------------------------------------------------
# Flat endpoints
# ---------------------------------------------------------------------------


get_filters: SubscriptableEndpoint[list[Filter], None, None, Filter] = SubscriptableEndpoint(
    "GET",
    "/api/v2/filters",
    list[Filter],
    "/api/v2/filters/{id}",
    Filter,
    requires="4.0.0",
    item_requires="4.0.0",
)

post_filters: Endpoint[Filter, None, _CreateFilterBody] = Endpoint(
    "POST",
    "/api/v2/filters",
    Filter,
    body=_CreateFilterBody,
    requires="4.0.0",
)

put_filters: EndpointTemplate[Filter, None, _UpdateFilterBody] = EndpointTemplate(
    "PUT",
    "/api/v2/filters/{id}",
    Filter,
    body=_UpdateFilterBody,
    requires="4.0.0",
)

delete_filters: EndpointTemplate[dict, None, None] = EndpointTemplate(
    "DELETE",
    "/api/v2/filters/{id}",
    dict,
    requires="4.0.0",
)


# ---------------------------------------------------------------------------
# By-ID namespace
# ---------------------------------------------------------------------------


class _FiltersById:
    __slots__ = ("get_keywords", "get_statuses", "post_keywords", "post_statuses")

    def __init__(self, filter_id: str, /) -> None:
        p = f"/api/v2/filters/{filter_id}"

        self.get_keywords: Endpoint[list[FilterKeyword], None, None] = Endpoint(
            "GET",
            f"{p}/keywords",
            list[FilterKeyword],
            requires="4.0.0",
        )
        self.post_keywords: Endpoint[FilterKeyword, None, _CreateKeywordBody] = Endpoint(
            "POST",
            f"{p}/keywords",
            FilterKeyword,
            body=_CreateKeywordBody,
            requires="4.0.0",
        )
        self.get_statuses: Endpoint[list[FilterStatus], None, None] = Endpoint(
            "GET",
            f"{p}/statuses",
            list[FilterStatus],
            requires="4.0.0",
        )
        self.post_statuses: Endpoint[FilterStatus, None, _CreateFilterStatusBody] = Endpoint(
            "POST",
            f"{p}/statuses",
            FilterStatus,
            body=_CreateFilterStatusBody,
            requires="4.0.0",
        )


class _FilterKeywordsNamespace:
    __slots__ = ()

    get: EndpointTemplate[FilterKeyword, None, None] = EndpointTemplate(
        "GET",
        "/api/v2/filters/keywords/{id}",
        FilterKeyword,
        requires="4.0.0",
    )
    put: EndpointTemplate[FilterKeyword, None, _CreateKeywordBody] = EndpointTemplate(
        "PUT",
        "/api/v2/filters/keywords/{id}",
        FilterKeyword,
        body=_CreateKeywordBody,
        requires="4.0.0",
    )
    delete: EndpointTemplate[dict, None, None] = EndpointTemplate(
        "DELETE",
        "/api/v2/filters/keywords/{id}",
        dict,
        requires="4.0.0",
    )


class _FilterStatusesNamespace:
    __slots__ = ()

    get: EndpointTemplate[FilterStatus, None, None] = EndpointTemplate(
        "GET",
        "/api/v2/filters/statuses/{id}",
        FilterStatus,
        requires="4.0.0",
    )
    delete: EndpointTemplate[FilterStatus, None, None] = EndpointTemplate(
        "DELETE",
        "/api/v2/filters/statuses/{id}",
        FilterStatus,
        requires="4.0.0",
    )


class _FiltersNamespace:
    __slots__ = ()

    keywords = _FilterKeywordsNamespace()
    statuses = _FilterStatusesNamespace()

    def __getitem__(self, filter_id: str) -> _FiltersById:
        return _FiltersById(filter_id)


filters = _FiltersNamespace()
