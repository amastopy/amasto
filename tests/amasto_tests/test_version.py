from __future__ import annotations
import pytest

from pydantic import BaseModel

from amasto._version import Unsupported, requires, since, unsupported


def test_since() -> None:

    @since("0.1.0")
    class Foo(BaseModel):
        foo: str | Unsupported = since("0.1.0")
        bar: str | Unsupported = since("0.2.0")

    foo = Foo(foo="foo")
    assert foo.foo == "foo"
    assert foo.bar is unsupported


@pytest.mark.asyncio
async def test_requires() -> None:
    # TODO: this test is currently a no-op since the version check is not yet implemented, but it should be updated to verify that UnsupportedVersionError is raised when the server version is too old.

    @requires("0.1.0")
    async def foo() -> str:
        return "foo"

    assert await foo() == "foo"
