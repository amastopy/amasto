from __future__ import annotations

from collections.abc import AsyncIterator
from pydantic import TypeAdapter
import re
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

if TYPE_CHECKING:
    from ._client import Amasto

__all__ = ("PaginatedHttpMethod",)

_LINK_NEXT_RE = re.compile(r'<([^>]+)>;\s*rel="next"')


def _parse_next_link(header: str | None) -> str | None:
    """Extract the ``rel="next"`` URL path+query from a ``Link`` header.

    Returns only the *path* component (with query string) so that the
    client never follows a redirect to an external host.
    """
    if header is None:
        return None
    match = _LINK_NEXT_RE.search(header)
    if match is None:
        return None
    parsed = urlparse(match.group(1))
    path = parsed.path
    if parsed.query:
        path = f"{path}?{parsed.query}"
    return path


class PaginatedHttpMethod[T, P = None]:
    """``HttpMethod`` subclass for list endpoints that support cursor-based pagination.

    The type parameter ``T`` is the **item** type (e.g. ``Status``), not
    ``list[Status]``.  Calling the instance (``await method(...)``) returns
    ``list[T]`` — identical to the previous behaviour.  The new
    ``.paginate()`` async iterator transparently follows ``Link: rel="next"``
    headers and yields individual items.

    Type parameters
    ---------------
    T
        The individual item type (a Pydantic model or ``str``).
    P : TypedDict | None
        Query-parameter shape.  ``None`` means no query params.
    """

    __slots__ = ("_adapter", "_client", "method", "path", "requires")

    method: str
    path: str
    requires: str | None

    def __init__(
        self,
        client: Amasto,
        method: str,
        path: str,
        model: type[T],
        /,
        *,
        requires: str | None = None,
    ) -> None:
        self._client = client
        self.method = method
        self.path = path
        self._adapter: TypeAdapter[list[T]] = TypeAdapter(list[model])
        self.requires = requires

    # ------------------------------------------------------------------
    # Single-page execution (backwards compatible)
    # ------------------------------------------------------------------

    async def __call__(
        self,
        *,
        params: P | None = None,
    ) -> list[T]:
        """Execute the HTTP request and return a single page as ``list[T]``."""
        if not self._client._initialized:  # noqa: SLF001
            raise RuntimeError("Client is not initialized")

        response = await self._client._http.request(  # noqa: SLF001
            self.method,
            self.path,
            params=params,  # type: ignore[arg-type]
        )
        response.raise_for_status()
        return self._adapter.validate_python(response.json())

    # ------------------------------------------------------------------
    # Paginated iteration
    # ------------------------------------------------------------------

    async def paginate(
        self,
        *,
        params: P | None = None,
        max_items: int | None = None,
    ) -> AsyncIterator[T]:
        """Async iterator that follows ``Link: rel="next"`` across pages.

        Parameters
        ----------
        params
            Query parameters for the **first** request.  Subsequent pages
            use the cursor embedded in the ``Link`` header URL.
        max_items
            Stop after yielding this many items.  ``None`` means unlimited.

        Yields
        ------
        T
            Individual items from each page.
        """
        if not self._client._initialized:  # noqa: SLF001
            raise RuntimeError("Client is not initialized")

        path: str | None = self.path
        query_params: Any = params
        yielded = 0

        while path is not None:
            response = await self._client._http.request(  # noqa: SLF001
                self.method,
                path,
                params=query_params,
            )
            response.raise_for_status()

            items = self._adapter.validate_python(response.json())
            if not items:
                return

            for item in items:
                yield item
                yielded += 1
                if max_items is not None and yielded >= max_items:
                    return

            # Only the first request uses caller-supplied params; subsequent
            # pages use the full path+query from the Link header directly.
            next_link = _parse_next_link(response.headers.get("link"))
            if next_link is None:
                return
            path = next_link
            query_params = None

    # ------------------------------------------------------------------
    # Parsing (for tests without HTTP)
    # ------------------------------------------------------------------

    def parse(self, data: list[dict[str, object]]) -> list[T]:
        """Validate *data* against ``list[T]`` (no HTTP)."""
        return self._adapter.validate_python(data)
