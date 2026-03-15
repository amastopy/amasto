# Contributing

Thank you for taking the time to contribute to **amasto**. This document explains how to set up a development environment, the conventions to follow, and the process for getting changes merged.

---

## Development Setup

**Prerequisites:** Python 3.14+, [`uv`](https://docs.astral.sh/uv/)

```bash
git clone https://github.com/amastopy/amasto.git
cd amasto

# Create a virtual environment and install dev dependencies
uv sync --dev

# Verify everything works
uv run pytest
```

---

## Project Conventions

### Async-first

All library code that touches I/O must be `async`. Do not add synchronous wrappers — callers can use `asyncio.run()` themselves if needed. There are no exceptions to this rule inside the `amasto` package itself.

### Type Annotations

Every public function, method, and class must be fully annotated. Run [`ty`](https://docs.astral.sh/ty/) before opening a pull request:

```bash
uv run ty check src/
```

### Code Style

The project uses `ruff` for both linting and formatting.

```bash
uv run ruff check src/ tests/
uv run ruff format src/ tests/
```

A pre-commit hook configuration is provided (see `.pre-commit-config.yaml`). Install it once with:

```bash
uv run pre-commit install
```

### Adding a New API Endpoint

1. Identify which namespace file under `api/` the endpoint belongs to (e.g. `api/statuses.py`). Create a new file if the topic does not exist yet.
2. Add a `models/` class for any new response type, using a Pydantic `BaseModel` with `frozen=True`.
3. Add the method to the namespace class. Use keyword-only parameters for all optional arguments.
4. Export any new public model from `models/__init__.py` and re-export from the top-level `amasto/__init__.py`.
5. Write tests in `tests/` (see *Testing* below).

---

## Testing

Tests live in `tests/` and use `pytest` with `pytest-asyncio` and `respx` to mock HTTP calls. No real network requests are made in the test suite.

```bash
uv run pytest                  # all tests
uv run pytest -x               # stop on first failure
uv run pytest tests/api/       # one subdirectory
```

### Writing a Test

```python
import pytest
import respx
import httpx
from amasto import MastoClient

@pytest.mark.asyncio
async def test_verify_credentials():
    with respx.mock:
        respx.get("https://mastodon.social/api/v1/accounts/verify_credentials").mock(
            return_value=httpx.Response(200, json={"id": "1", "username": "alice", ...})
        )
        async with MastoClient(instance="mastodon.social", access_token="test") as client:
            account = await client.accounts.verify_credentials()
        assert account.username == "alice"
```

Guidelines:
- One test file per module (e.g. `tests/api/test_accounts.py` for `api/accounts.py`).
- Test error paths (4xx, 5xx, rate-limit) as well as the happy path.
- Do not use `time.sleep` or `await asyncio.sleep` in tests; mock time-dependent behaviour instead.

---

## Pull Request Process

1. Fork the repository and create a feature branch off `main`:
   ```bash
   git checkout -b feat/my-feature
   ```
2. Make your changes, ensuring all tests pass and linting is clean.
3. Open a pull request against `main`. Fill in the PR template.
4. At least one maintainer review is required before merging.
5. Squash-merge is preferred for small changes; merge commits are acceptable for larger feature work.

---

## Reporting Issues

Please include:
- Python version (`python --version`)
- amasto version (`python -c "import amasto; print(amasto.__version__)"`)
- A minimal reproducible example
- The full traceback
