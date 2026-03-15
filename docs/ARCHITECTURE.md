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
├── __init__.py          # Public re-exports only
├── py.typed
│
├── client.py            # MastoClient — the main entry point
├── auth.py              # OAuth 2.0 authorisation flow
├── exceptions.py        # Hierarchy of library-specific exceptions
├── _http.py             # Internal HTTP layer (rate-limit, retry, error mapping)
│
├── models/              # Pydantic v2 response models
│   ├── __init__.py
│   ├── account.py
│   ├── status.py
│   ├── notification.py
│   ├── media.py
│   └── ...
│
└── api/                 # Per-topic API mixin / namespace classes
    ├── __init__.py
    ├── accounts.py
    ├── statuses.py
    ├── timelines.py
    ├── notifications.py
    ├── media.py
    └── streaming.py
```

### `client.py` — `MastoClient`

`MastoClient` is the single object users interact with. It is an `async` context manager that owns an `httpx.AsyncClient` for its lifetime.

```python
async with MastoClient(instance="mastodon.social", access_token="…") as client:
    me = await client.accounts.verify_credentials()
    async for event in client.streaming.user():
        print(event)
```

Internally, `MastoClient` composes the API namespace objects (`self.accounts`, `self.statuses`, …) and injects the shared `_http.HTTPSession` into each.

### `_http.py` — `HTTPSession`

All outbound requests go through `HTTPSession`. It is responsible for:

- Attaching the `Authorization: Bearer …` header.
- Respecting `X-RateLimit-*` headers and back-off automatically.
- Mapping non-2xx responses to the correct `MastoError` subclass.
- Retrying idempotent requests on transient 5xx / network errors (configurable; off by default).

`HTTPSession` is an **internal** type and is not part of the public API.

### `api/` — API Namespaces

Each file in `api/` corresponds to one section of the Mastodon REST API. Classes here are pure method containers with no state of their own; they hold a reference to the shared `HTTPSession`.

Methods follow a consistent signature pattern:

```python
async def get_account(self, account_id: str) -> Account: ...
async def get_statuses(
    self,
    account_id: str,
    *,
    max_id: str | None = None,
    limit: int = 20,
) -> list[Status]: ...
```

- Keyword-only parameters (`*`) are used for all optional filters/pagination arguments.
- Paginated endpoints return `list[T]` and expose a cursor-based helper (see *Pagination* below).

### `models/` — Response Models

Response models are **Pydantic v2** `BaseModel` subclasses. They are read-only (`model_config = ConfigDict(frozen=True)`).

Field names follow the Mastodon API's snake_case JSON keys directly so that `model_validate(json_data)` works without a custom alias.

### `auth.py` — OAuth 2.0

Provides helpers for both the **authorisation code** flow (for apps acting on behalf of users) and the **client credentials** flow (for server-side apps).

```python
app = await MastoApp.register(instance="mastodon.social", client_name="my-app")
url = app.authorisation_url(scopes=["read", "write"])
token = await app.fetch_token(code="…")
```

### `api/streaming.py` — Streaming

The Mastodon streaming API is accessed over a persistent HTTP connection using Server-Sent Events (SSE). `httpx` supports streaming response bodies natively, so the implementation uses an `async` generator:

```python
async def user(self) -> AsyncGenerator[StreamEvent, None]:
    async with self._http.stream("GET", "/api/v1/streaming/user") as response:
        async for line in response.aiter_lines():
            if event := _parse_sse(line):
                yield event
```

---

## Pagination

Mastodon's list endpoints are paginated via `Link` headers (not query parameters). A `Paginator[T]` async generator is provided to iterate transparently:

```python
async for status in client.timelines.home.paginate():
    process(status)
```

`Paginator` yields individual items and follows `next` links automatically until exhausted or the caller breaks.

---

## Error Hierarchy

```
MastoError
├── HTTPError
│   ├── ClientError        # 4xx
│   │   ├── AuthError      # 401 / 403
│   │   ├── NotFoundError  # 404
│   │   └── RateLimitError # 429
│   └── ServerError        # 5xx
└── StreamError            # Streaming connection lost / malformed event
```

---

## Python Version Policy

The minimum supported version is **Python 3.14** (as declared in `pyproject.toml`). Features added in 3.14 (e.g. improved `asyncio` internals, `type` statement for type aliases) may be used freely.

---

## Dependency Policy

| Dependency | Reason | Scope |
|---|---|---|
| `httpx` | Async HTTP client, HTTP/2, SSE streaming | Runtime |
| `pydantic` | Response model validation & serialisation | Runtime |
| `pytest` + `pytest-asyncio` | Test runner | Dev |
| `respx` | Mock `httpx` in tests | Dev |

Runtime dependencies are kept minimal. Optional extras (e.g. `amasto[cli]`) may be introduced later for non-essential integrations.
