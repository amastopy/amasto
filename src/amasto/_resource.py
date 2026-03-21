from __future__ import annotations

from pydantic import TypeAdapter
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ._client import Amasto

__all__ = ("HttpMethod",)


class HttpMethod[T, P = None, B = None]:
    """Async-callable HTTP method bound to a client and a concrete path.

    Replaces the former ``Endpoint`` descriptor.  Each instance knows its
    HTTP verb, request path, and response type so it can execute the
    request **and** validate the response in a single ``await`` call.

    Type parameters
    ---------------
    T
        The response type (a Pydantic model or ``list[Model]``).
    P : TypedDict | None
        Query-parameter shape.  ``None`` means no query params.
    B : TypedDict | None
        JSON-body shape.  ``None`` means no request body.
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
        self._adapter: TypeAdapter[T] = TypeAdapter(model)
        self.requires = requires

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    async def __call__(
        self,
        *,
        params: P | None = None,
        body: B | None = None,
        raw: dict[str, Any] | None = None,
    ) -> T:
        """Execute the HTTP request and return a validated response."""
        await self._client._initialization_event.wait()  # noqa: SLF001

        response = await self._client._http.request(  # noqa: SLF001
            self.method,
            self.path,
            params=params,  # type: ignore[arg-type]
            json=body,
        )
        response.raise_for_status()

        data: Any = response.json()

        if raw is not None and isinstance(data, dict):
            raw.update(data)

        return self._adapter.validate_python(data)

    # ------------------------------------------------------------------
    # Parsing (for tests without HTTP)
    # ------------------------------------------------------------------

    def parse(self, data: Any) -> T:  # noqa: ANN401
        """Validate *data* against the response type (no HTTP)."""
        return self._adapter.validate_python(data)
