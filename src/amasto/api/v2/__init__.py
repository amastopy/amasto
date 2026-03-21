from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("V2Namespace",)


class V2Namespace:
    __slots__ = (
        "filters",
        "instance",
        "media",
        "notifications",
        "search",
        "suggestions",
    )

    def __init__(self, client: Amasto, /) -> None:
        from ._filters import FiltersResource
        from ._instance import InstanceResource
        from ._media import MediaResource
        from ._notifications import NotificationsResource
        from ._search import SearchResource
        from ._suggestions import SuggestionsResource

        self.filters = FiltersResource(client)
        self.instance = InstanceResource(client)
        self.media = MediaResource(client)
        self.notifications = NotificationsResource(client)
        self.search = SearchResource(client)
        self.suggestions = SuggestionsResource(client)
