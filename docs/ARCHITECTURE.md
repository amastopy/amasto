# Architecture

This document describes the design decisions and module structure of **amasto**, an async-first Python library for the Mastodon API.

## Guiding Principles

1. **Async-first** — All I/O is `async`/`await`. No synchronous counterparts are provided. Callers who need synchronous behaviour can wrap calls in `asyncio.run()` themselves.
2. **Type-safe** — Every public interface is fully annotated. The `py.typed` marker is shipped so downstream users get complete type checking out of the box.
3. **Minimal surface area** — The public API exposed from `amasto` is small and deliberate. Implementation details live in `_`-prefixed modules.
4. **Single dependency for HTTP** — `httpx` is chosen as the HTTP client. It supports HTTP/2, full async semantics, and exposes the primitives needed for streaming without a separate library.

---

## Module Layout

```
src/amasto/
├── __init__.py           # Public re-exports: Amasto, models
├── py.typed
├── _client.py            # Amasto — the main entry point
├── _resource.py          # HttpMethod[T, P, B] — async-callable HTTP method
├── _pagination.py        # PaginatedHttpMethod[T, P] — cursor-based pagination
├── _nodeinfo.py          # NodeInfo auto-discovery
├── _params.py            # Shared TypedDicts (e.g. PaginationParams)
├── _version.py           # since() / Unsupported version-awareness helpers
├── _streaming.py         # WebSocket streaming dispatcher + reconnection
│
├── models/               # Pydantic v2 response models
│   ├── __init__.py       # Re-exports from v1 + v2
│   ├── v1/               # V1 API models
│   └── v2/               # V2 API models
│
├── api/                  # Resource-based API namespaces
│   ├── __init__.py       # ApiNamespace(client) — composes v1, v2, oembed
│   ├── _oembed.py        # OEmbedResource
│   ├── v1/
│   │   ├── __init__.py   # V1Namespace(client) — composes all 33 resources
│   │   ├── _accounts.py  # AccountsResource
│   │   ├── _statuses.py  # StatusesResource
│   │   ├── _streaming.py # StreamingResource
│   │   └── ...
│   └── v2/
│       ├── __init__.py   # V2Namespace(client) — composes 6 resources
│       ├── _filters.py   # FiltersResource
│       └── ...
│
├── oauth/                # OAuth namespace
│   ├── __init__.py       # OAuthNamespace(client)
│   ├── _authorize.py     # AuthorizeResource
│   ├── _token.py         # TokenResource
│   ├── _revoke.py        # RevokeResource
│   └── _userinfo.py      # UserinfoResource
│
└── health/               # Health endpoint
    ├── __init__.py
    └── _health.py        # HealthResource
```

### `_client.py` — `Amasto`

`Amasto` is the single object users interact with. It owns an `httpx.AsyncClient` and automatically discovers the server's Mastodon version via the NodeInfo protocol on first use.

```python
client = Amasto("https://mastodon.social", "YOUR_ACCESS_TOKEN")

# All endpoints are accessed through attribute chains:
status = await client.api.v1.statuses["123"].get()
accounts = await client.api.v1.accounts["123"].followers.get()
```

`Amasto.__init__` lazily imports and constructs:
- `self.api` → `ApiNamespace(self)` → `V1Namespace`, `V2Namespace`, `OEmbedResource`
- `self.oauth` → `OAuthNamespace(self)` → `AuthorizeResource`, `TokenResource`, …
- `self.health` → `HealthResource(self)`

During `_initialize()`, `Amasto` also calls `/api/v1/instance` to discover the WebSocket streaming URL and stores it as `_streaming_url`.

Lazy imports in `__init__` prevent circular dependency issues since resource files reference the `Amasto` type for type checking.

### `_resource.py` — `HttpMethod[T, P, B]`

The core building block. Each `HttpMethod` instance binds:
- A reference to the owning `Amasto` client (for HTTP and version info)
- The HTTP verb (`GET`, `POST`, etc.)
- The URL path
- The response type (validated via `pydantic.TypeAdapter`)
- An optional minimum server version (`requires`)

`HttpMethod` is async-callable:

```python
# Execute HTTP request and return validated response
result: T = await method(params=..., body=...)

# Validate data without HTTP (useful in tests)
result: T = method.parse(data)
```

### `_pagination.py` — `PaginatedHttpMethod[T, P]`

A specialisation of `HttpMethod` for list endpoints that support Mastodon's cursor-based pagination via `Link` headers.  `T` is the **item** type (e.g. `Status`), not `list[Status]`.

```python
# Single page (backwards compatible)
statuses: list[Status] = await client.api.v1.timelines.home.get()

# Async iteration across all pages
async for status in client.api.v1.timelines.home.get.paginate(params={"limit": 40}):
    print(status.content)

# Stop after N items
async for status in client.api.v1.timelines.home.get.paginate(max_items=200):
    print(status.content)
```

Internally, `.paginate()` parses the `Link: rel="next"` response header after each page and extracts only the path + query string (never following external hosts).

### Resource Classes

Each resource file defines one or more small classes with `__slots__` that compose `HttpMethod` or `PaginatedHttpMethod` instances as attributes:

```python
class BookmarksResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: PaginatedHttpMethod[Status, PaginationParams] = PaginatedHttpMethod(
            client, "GET", "/api/v1/bookmarks", Status,
        )
```

For resources with sub-resources or per-ID access, `__getitem__` returns a nested resource:

```python
class AccountsResource:
    __slots__ = ("_client", "get", "post", "verify_credentials", ...)

    def __init__(self, client: Amasto, /) -> None:
        self._client = client
        self.get = HttpMethod(client, "GET", "/api/v1/accounts", list[Account])
        self.verify_credentials = _VerifyCredentialsResource(client)
        ...

    def __getitem__(self, id: str) -> _AccountByIdResource:
        return _AccountByIdResource(self._client, id)
```

### `models/` — Response Models

Response models are **Pydantic v2** `BaseModel` subclasses. They are read-only (`model_config = ConfigDict(frozen=True)`).

Field names follow the Mastodon API's snake_case JSON keys directly so that `model_validate(json_data)` works without a custom alias.

---

## Version Awareness

Model fields annotated with `since("x.y.z")` resolve to `Unsupported` when the connected server is older than the specified version.

Endpoints can declare `requires="x.y.z"` to indicate the minimum server version needed for the endpoint.

---

## Streaming

Real-time streaming uses `websockets` over a persistent WebSocket connection to the Mastodon streaming endpoint.

### Architecture

- **`_streaming.py`** — Low-level async generator `stream_events()` that manages the WebSocket lifecycle: connection, subscribe message, event dispatch, and automatic reconnection with exponential back-off via `ReconnectPolicy`.
- **`api/v1/_streaming.py`** — `StreamingResource` exposed as `client.api.v1.streaming`. Provides named methods (`user()`, `public()`, `hashtag(tag)`, etc.) that delegate to `stream_events()`.
- **`models/v1/_stream_event.py`** — 11 typed Pydantic event models plus `StreamEvent` type alias.

### Protocol

1. The WebSocket endpoint URL (`wss://...`) is discovered during client initialisation from the `/api/v1/instance` response (`urls.streaming_api`).
2. Authentication is performed via the `Authorization: Bearer` header on the WebSocket handshake.
3. After connecting, a `{"type": "subscribe", "stream": "..."}` JSON message is sent to select the stream.
4. Incoming messages have the shape `{"stream": [...], "event": "...", "payload": "..."}`. The `payload` is a string-encoded JSON for most events; `delete` and `announcement.delete` payloads are plain string IDs.
5. On connection loss, the generator sleeps with exponential back-off (configurable via `ReconnectPolicy`) and reconnects. HTTP 4xx handshake errors propagate immediately.

---

## Python Version Policy

The minimum supported version is **Python 3.14** (as declared in `pyproject.toml`). Features added in 3.14 (e.g. improved `asyncio` internals, generic class syntax) may be used freely.

---

## Dependency Policy

| Dependency | Reason | Scope |
|---|---|---|
| `httpx` | Async HTTP client | Runtime |
| `pydantic` | Response model validation & serialisation | Runtime |
| `semver` | Server version parsing | Runtime |
| `websockets` | WebSocket streaming | Runtime |
| `pytest` + `pytest-asyncio` | Test runner | Dev |
| `respx` | Mock `httpx` in tests | Dev |
| `ruff` | Linter & formatter | Dev |

Runtime dependencies are kept minimal.
