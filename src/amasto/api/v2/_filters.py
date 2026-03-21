from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v2 import Filter, FilterKeyword, FilterStatus
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("FiltersResource",)


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
# Top-level keyword / status lookups  (filters.keywords["id"])
# ---------------------------------------------------------------------------


class _FilterKeywordByIdResource:
    __slots__ = ("delete", "get", "put")

    def __init__(self, client: Amasto, keyword_id: str, /) -> None:
        p = f"/api/v2/filters/keywords/{keyword_id}"
        self.get: HttpMethod[FilterKeyword, None, None] = HttpMethod(
            client,
            "GET",
            p,
            FilterKeyword,
            requires="4.0.0",
        )
        self.put: HttpMethod[FilterKeyword, None, _CreateKeywordBody] = HttpMethod(
            client,
            "PUT",
            p,
            FilterKeyword,
            requires="4.0.0",
        )
        self.delete: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "DELETE",
            p,
            dict,
            requires="4.0.0",
        )


class _FilterKeywordsTopResource:
    __slots__ = ("_client",)

    def __init__(self, client: Amasto, /) -> None:
        self._client = client

    def __getitem__(self, keyword_id: str) -> _FilterKeywordByIdResource:
        return _FilterKeywordByIdResource(self._client, keyword_id)


class _FilterStatusByIdResource:
    __slots__ = ("delete", "get")

    def __init__(self, client: Amasto, status_id: str, /) -> None:
        p = f"/api/v2/filters/statuses/{status_id}"
        self.get: HttpMethod[FilterStatus, None, None] = HttpMethod(
            client,
            "GET",
            p,
            FilterStatus,
            requires="4.0.0",
        )
        self.delete: HttpMethod[FilterStatus, None, None] = HttpMethod(
            client,
            "DELETE",
            p,
            FilterStatus,
            requires="4.0.0",
        )


class _FilterStatusesTopResource:
    __slots__ = ("_client",)

    def __init__(self, client: Amasto, /) -> None:
        self._client = client

    def __getitem__(self, status_id: str) -> _FilterStatusByIdResource:
        return _FilterStatusByIdResource(self._client, status_id)


# ---------------------------------------------------------------------------
# Per-filter sub-resources  (filters["filter_id"].keywords / .statuses)
# ---------------------------------------------------------------------------


class _FilterKeywordsSubResource:
    __slots__ = ("get", "post")

    def __init__(self, client: Amasto, filter_id: str, /) -> None:
        p = f"/api/v2/filters/{filter_id}/keywords"
        self.get: HttpMethod[list[FilterKeyword], None, None] = HttpMethod(
            client,
            "GET",
            p,
            list[FilterKeyword],
            requires="4.0.0",
        )
        self.post: HttpMethod[FilterKeyword, None, _CreateKeywordBody] = HttpMethod(
            client,
            "POST",
            p,
            FilterKeyword,
            requires="4.0.0",
        )


class _FilterStatusesSubResource:
    __slots__ = ("get", "post")

    def __init__(self, client: Amasto, filter_id: str, /) -> None:
        p = f"/api/v2/filters/{filter_id}/statuses"
        self.get: HttpMethod[list[FilterStatus], None, None] = HttpMethod(
            client,
            "GET",
            p,
            list[FilterStatus],
            requires="4.0.0",
        )
        self.post: HttpMethod[FilterStatus, None, _CreateFilterStatusBody] = HttpMethod(
            client,
            "POST",
            p,
            FilterStatus,
            requires="4.0.0",
        )


class _FilterByIdResource:
    __slots__ = ("delete", "get", "keywords", "put", "statuses")

    def __init__(self, client: Amasto, filter_id: str, /) -> None:
        p = f"/api/v2/filters/{filter_id}"
        self.get: HttpMethod[Filter, None, None] = HttpMethod(
            client,
            "GET",
            p,
            Filter,
            requires="4.0.0",
        )
        self.put: HttpMethod[Filter, None, _UpdateFilterBody] = HttpMethod(
            client,
            "PUT",
            p,
            Filter,
            requires="4.0.0",
        )
        self.delete: HttpMethod[dict, None, None] = HttpMethod(
            client,
            "DELETE",
            p,
            dict,
            requires="4.0.0",
        )
        self.keywords = _FilterKeywordsSubResource(client, filter_id)
        self.statuses = _FilterStatusesSubResource(client, filter_id)


# ---------------------------------------------------------------------------
# Top-level resource
# ---------------------------------------------------------------------------


class FiltersResource:
    __slots__ = ("_client", "get", "keywords", "post", "statuses")

    def __init__(self, client: Amasto, /) -> None:
        self._client = client
        self.get: HttpMethod[list[Filter], None, None] = HttpMethod(
            client,
            "GET",
            "/api/v2/filters",
            list[Filter],
            requires="4.0.0",
        )
        self.post: HttpMethod[Filter, None, _CreateFilterBody] = HttpMethod(
            client,
            "POST",
            "/api/v2/filters",
            Filter,
            requires="4.0.0",
        )
        self.keywords = _FilterKeywordsTopResource(client)
        self.statuses = _FilterStatusesTopResource(client)

    def __getitem__(self, filter_id: str) -> _FilterByIdResource:
        return _FilterByIdResource(self._client, filter_id)
