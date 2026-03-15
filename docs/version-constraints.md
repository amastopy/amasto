# Version Constraints

The Mastodon API evolves across server versions — fields, entities, and endpoints may not exist on older instances. This document defines how `amasto` represents and enforces these version constraints.

---

## Overview

Version constraints apply at three levels, using two tools:

| Level | Tool | Behaviour |
|---|---|---|
| Field | `since()` as field default | Metadata only — falls back to `None` |
| Entity | `@since()` as class decorator | Metadata only — no runtime effect |
| Endpoint | `@requires()` as method decorator | Raises `UnsupportedVersionError` on call |

`since()` is for **soft** constraints (documents the version, does not enforce it). `requires()` is for **hard** constraints (blocks the call if the server is too old).

---

## `since()` — Soft Constraints

### On fields

Version-constrained fields use `since()` as the default value. When the server does not provide the field (because its version is too old), the field is set to the `UNSUPPORTED` sentinel rather than `None`. This keeps `None` unambiguous — it always means "the field is supported but has no value".

```python
from pydantic import BaseModel, ConfigDict
from amasto._version import since, Unsupported

class Status(BaseModel):
    model_config = ConfigDict(frozen=True)

    # Present in all versions → plain annotation
    id: str
    content: str
    spoiler_text: str

    # Only present from a specific version onwards → since()
    # str | Unsupported: supported and non-null, or unsupported
    text: str | Unsupported = since("4.0.0")
    edited_at: str | Unsupported = since("4.0.0")
    local_only: bool | Unsupported = since("4.2.0")

    # Nullable AND version-constrained → str | None | Unsupported
    content_map: dict | None | Unsupported = since("4.2.0")
```

`since(version)` returns `Field(default=UNSUPPORTED, metadata=[Since(version)])` internally. From Pydantic's perspective it behaves identically to a regular `Field`.

Fields that are nullable but have no version constraint still use plain `None`:

```python
in_reply_to_id: str | None = None  # supported in all versions, but may be absent
```

In user code, the three states are distinct and checkable:

```python
match status.text:
    case str() as t:
        print(t)         # supported, has a value
    case None:
        pass             # supported, no value
    case Unsupported():
        pass             # server too old to support this field
```

### On entities

When an entire entity was introduced in a specific version, decorate the class with `@since()`. This attaches a `Since` instance as a class attribute (`__since__`) with no other runtime effect.

```python
from amasto._version import since

@since("4.0.0")
class Poll(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    expires_at: str | None = None
```

---

## `@requires()` — Hard Constraints

Endpoints that do not exist below a certain server version use `@requires()`. Unlike `@since()`, this decorator wraps the coroutine and automatically raises `UnsupportedVersionError` before the HTTP request is made.

```python
from amasto._version import requires

class PollsAPI:
    @requires("4.0.0")
    async def get(self, poll_id: str) -> Poll: ...
```

`MastoClient` parses the server version from `/api/v2/instance` on connect and stores it in the `server_version` attribute. `@requires()` checks this value at call time.

For ad-hoc version guards in user code, `client.require()` is also available:

```python
async with MastoClient(instance="mastodon.social") as client:
    status = await client.statuses.get(status_id)

    # Without a version guard → None check required
    if status.text is not None:
        print(status.text)

    # With a version guard → raises UnsupportedVersionError on servers below 4.0.0
    client.require("4.0.0")
    print(status.text)  # guaranteed not to be None (explicit narrowing still required)
```

---

## Why Two Separate Names?

`since()` returns a `FieldInfo` when used as a field default, and attaches a class attribute when used as a class decorator. These two uses are expressible via `@overload`. However, combining endpoint behaviour — which requires wrapping a coroutine — into the same name would force the return type to vary between `FieldInfo`, a class, and a coroutine function depending on context. That is not expressible cleanly in the type system.

The naming also reflects intent: `@since` means "document this", `@requires` means "guard this".

---

## Accessing Metadata

`Since` objects can be accessed via Pydantic's `model_fields` (for fields) or `__since__` (for entities). This is useful for automated documentation generation or runtime introspection.

```python
from amasto._version import Since
from amasto.models import Status

for name, field in Status.model_fields.items():
    for meta in field.metadata:
        if isinstance(meta, Since):
            print(f"{name}: requires >= {meta.version}")
# text: requires >= 4.0.0
# edited_at: requires >= 4.0.0
# local_only: requires >= 4.2.0
```

---

## Checklist

### Adding a new field

1. Check the [Mastodon API documentation](https://docs.joinmastodon.org/entities/) to find the version in which the field was introduced.
2. If the field has a version constraint, use `since("X.Y.Z")` and include `Unsupported` in the type: `T | Unsupported`.
3. If the field is also genuinely nullable, include `None` as well: `T | None | Unsupported`.
4. If there is no version constraint, use a plain annotation. Use `T | None` if the value may be absent.

### Adding a new entity

1. Check the version in which the entity was introduced.
2. Decorate the class with `@since("X.Y.Z")`.
3. Apply the field rules above to each field within the entity.

### Adding a new endpoint

1. Check the version in which the endpoint was introduced.
2. Decorate the method with `@requires("X.Y.Z")`.
3. If the endpoint returns a versioned entity, ensure the entity class has `@since()`.
