from __future__ import annotations

from amasto._nodeinfo import (
    _NODEINFO_SCHEMA_2_0,
    _NODEINFO_SCHEMA_2_1,
    Inbound,
    NodeInfo,
    Outbound,
    Protocol,
    Services,
    Software,
    Usage,
    Users,
)
import httpx
import pytest
import respx


def _make_nodeinfo_dict(
    *,
    version: str = "2.1",
    software_name: str = "mastodon",
    software_version: str = "4.0.0",
    protocols: list[str] | None = None,
    open_registrations: bool = True,
) -> dict:
    return {
        "version": version,
        "software": {
            "name": software_name,
            "version": software_version,
        },
        "protocols": protocols or ["activitypub"],
        "services": {"inbound": [], "outbound": []},
        "openRegistrations": open_registrations,
        "usage": {
            "users": {"total": 100, "activeHalfyear": 50, "activeMonth": 30},
            "localPosts": 1000,
            "localComments": 500,
        },
        "metadata": {},
    }


# MARK: - Model validation


def test_nodeinfo_model_validation() -> None:
    data = _make_nodeinfo_dict()
    info = NodeInfo.model_validate(data)
    assert info.version == "2.1"
    assert info.software.name == "mastodon"
    assert info.software.version == "4.0.0"
    assert info.protocols == [Protocol.ACTIVITYPUB]
    assert info.openRegistrations is True
    assert info.usage.localPosts == 1000
    assert info.metadata == {}


def test_nodeinfo_open_registrations_property() -> None:
    info = NodeInfo.model_validate(_make_nodeinfo_dict(open_registrations=False))
    assert info.open_registrations is False


def test_usage_properties() -> None:
    usage = Usage.model_validate(
        {
            "users": {"total": 100, "activeHalfyear": 50, "activeMonth": 30},
            "localPosts": 1000,
            "localComments": 500,
        }
    )
    assert usage.local_posts == 1000
    assert usage.local_comments == 500


def test_usage_optional_fields() -> None:
    usage = Usage.model_validate({"users": {}})
    assert usage.local_posts is None
    assert usage.local_comments is None


def test_users_properties() -> None:
    users = Users.model_validate({"total": 100, "activeHalfyear": 50, "activeMonth": 30})
    assert users.active_halfyear == 50
    assert users.active_month == 30


def test_users_optional_fields() -> None:
    users = Users.model_validate({})
    assert users.total is None
    assert users.active_halfyear is None
    assert users.active_month is None


def test_software_model() -> None:
    soft = Software.model_validate({"name": "mastodon", "version": "4.0.0"})
    assert soft.name == "mastodon"
    assert soft.version == "4.0.0"


def test_services_model() -> None:
    services = Services.model_validate({"inbound": ["imap", "pop3"], "outbound": ["smtp"]})
    assert services.inbound == [Inbound.IMAP, Inbound.POP3]
    assert services.outbound == [Outbound.SMTP]


def test_protocol_enum() -> None:
    assert Protocol("activitypub") is Protocol.ACTIVITYPUB
    assert Protocol("diaspora") is Protocol.DIASPORA


def test_multiple_protocols() -> None:
    info = NodeInfo.model_validate(_make_nodeinfo_dict(protocols=["activitypub", "diaspora"]))
    assert info.protocols == [Protocol.ACTIVITYPUB, Protocol.DIASPORA]


# MARK: - fetch()


def test_fetch_prefers_latest_schema() -> None:
    base_url = "https://mastodon.example"
    jrd = {
        "links": [
            {"rel": _NODEINFO_SCHEMA_2_0, "href": f"{base_url}/nodeinfo/2.0"},
            {"rel": _NODEINFO_SCHEMA_2_1, "href": f"{base_url}/nodeinfo/2.1"},
        ]
    }
    nodeinfo_data = _make_nodeinfo_dict()

    with respx.mock:
        respx.get(f"{base_url}/.well-known/nodeinfo").mock(return_value=httpx.Response(200, json=jrd))
        respx.get(f"{base_url}/nodeinfo/2.1").mock(return_value=httpx.Response(200, json=nodeinfo_data))
        info = NodeInfo.fetch(base_url)

    assert info.software.name == "mastodon"


def test_fetch_with_only_2_0_schema() -> None:
    base_url = "https://mastodon.example"
    jrd = {
        "links": [
            {"rel": _NODEINFO_SCHEMA_2_0, "href": f"{base_url}/nodeinfo/2.0"},
        ]
    }
    nodeinfo_data = _make_nodeinfo_dict(version="2.0")

    with respx.mock:
        respx.get(f"{base_url}/.well-known/nodeinfo").mock(return_value=httpx.Response(200, json=jrd))
        respx.get(f"{base_url}/nodeinfo/2.0").mock(return_value=httpx.Response(200, json=nodeinfo_data))
        info = NodeInfo.fetch(base_url)

    assert info.version == "2.0"


def test_fetch_no_supported_schema_raises() -> None:
    base_url = "https://mastodon.example"
    jrd = {
        "links": [
            {"rel": "http://unknown.schema/1.0", "href": f"{base_url}/nodeinfo/1.0"},
        ]
    }

    with respx.mock:
        respx.get(f"{base_url}/.well-known/nodeinfo").mock(return_value=httpx.Response(200, json=jrd))
        with pytest.raises(ValueError, match="No supported NodeInfo schema"):
            NodeInfo.fetch(base_url)


def test_fetch_empty_links_raises() -> None:
    base_url = "https://mastodon.example"
    jrd: dict = {"links": []}

    with respx.mock:
        respx.get(f"{base_url}/.well-known/nodeinfo").mock(return_value=httpx.Response(200, json=jrd))
        with pytest.raises(ValueError, match="No supported NodeInfo schema"):
            NodeInfo.fetch(base_url)


def test_fetch_missing_href_raises() -> None:
    base_url = "https://mastodon.example"
    jrd = {
        "links": [
            {"rel": _NODEINFO_SCHEMA_2_1},
        ]
    }

    with respx.mock:
        respx.get(f"{base_url}/.well-known/nodeinfo").mock(return_value=httpx.Response(200, json=jrd))
        with pytest.raises(ValueError, match="missing 'href' field"):
            NodeInfo.fetch(base_url)


def test_fetch_jrd_http_error_raises() -> None:
    base_url = "https://mastodon.example"

    with respx.mock:
        respx.get(f"{base_url}/.well-known/nodeinfo").mock(return_value=httpx.Response(500))
        with pytest.raises(httpx.HTTPStatusError):
            NodeInfo.fetch(base_url)


def test_fetch_mastodon_social() -> None:
    """Mock real responses from mastodon.social."""
    base_url = "https://mastodon.social"
    jrd = {
        "links": [
            {
                "rel": "http://nodeinfo.diaspora.software/ns/schema/2.0",
                "href": "https://mastodon.social/nodeinfo/2.0",
            }
        ]
    }
    nodeinfo_json = {
        "version": "2.0",
        "software": {"name": "mastodon", "version": "4.6.0-nightly.2026-03-16"},
        "protocols": ["activitypub"],
        "services": {"outbound": [], "inbound": []},
        "usage": {
            "users": {
                "total": 3183755,
                "activeMonth": 295867,
                "activeHalfyear": 714189,
            },
            "localPosts": 168505535,
        },
        "openRegistrations": True,
        "metadata": {
            "nodeName": "Mastodon",
            "nodeDescription": (
                "The original server of Mastodon, operated by Mastodon GmbH for the common good.\r\n\r\n"
            ),
        },
    }

    with respx.mock:
        respx.get(f"{base_url}/.well-known/nodeinfo").mock(return_value=httpx.Response(200, json=jrd))
        respx.get(f"{base_url}/nodeinfo/2.0").mock(return_value=httpx.Response(200, json=nodeinfo_json))
        info = NodeInfo.fetch(base_url)

    assert info.version == "2.0"
    assert info.software.name == "mastodon"
    assert info.software.version == "4.6.0-nightly.2026-03-16"
    assert info.protocols == [Protocol.ACTIVITYPUB]
    assert info.services.inbound == []
    assert info.services.outbound == []
    assert info.usage.users.total == 3183755
    assert info.usage.users.active_month == 295867
    assert info.usage.users.active_halfyear == 714189
    assert info.usage.local_posts == 168505535
    assert info.usage.local_comments is None
    assert info.open_registrations is True
    assert info.metadata["nodeName"] == "Mastodon"


# MARK: - afetch()


@pytest.mark.asyncio
async def test_afetch_prefers_latest_schema() -> None:
    base_url = "https://mastodon.example"
    jrd = {
        "links": [
            {"rel": _NODEINFO_SCHEMA_2_0, "href": f"{base_url}/nodeinfo/2.0"},
            {"rel": _NODEINFO_SCHEMA_2_1, "href": f"{base_url}/nodeinfo/2.1"},
        ]
    }
    nodeinfo_data = _make_nodeinfo_dict()

    with respx.mock:
        respx.get(f"{base_url}/.well-known/nodeinfo").mock(return_value=httpx.Response(200, json=jrd))
        respx.get(f"{base_url}/nodeinfo/2.1").mock(return_value=httpx.Response(200, json=nodeinfo_data))
        info = await NodeInfo.afetch(base_url)

    assert info.software.name == "mastodon"


@pytest.mark.asyncio
async def test_afetch_with_only_2_0_schema() -> None:
    base_url = "https://mastodon.example"
    jrd = {
        "links": [
            {"rel": _NODEINFO_SCHEMA_2_0, "href": f"{base_url}/nodeinfo/2.0"},
        ]
    }
    nodeinfo_data = _make_nodeinfo_dict(version="2.0")

    with respx.mock:
        respx.get(f"{base_url}/.well-known/nodeinfo").mock(return_value=httpx.Response(200, json=jrd))
        respx.get(f"{base_url}/nodeinfo/2.0").mock(return_value=httpx.Response(200, json=nodeinfo_data))
        info = await NodeInfo.afetch(base_url)

    assert info.version == "2.0"


@pytest.mark.asyncio
async def test_afetch_no_supported_schema_raises() -> None:
    base_url = "https://mastodon.example"
    jrd = {
        "links": [
            {"rel": "http://unknown.schema/1.0", "href": f"{base_url}/nodeinfo/1.0"},
        ]
    }

    with respx.mock:
        respx.get(f"{base_url}/.well-known/nodeinfo").mock(return_value=httpx.Response(200, json=jrd))
        with pytest.raises(ValueError, match="No supported NodeInfo schema"):
            await NodeInfo.afetch(base_url)


@pytest.mark.asyncio
async def test_afetch_missing_href_raises() -> None:
    base_url = "https://mastodon.example"
    jrd = {
        "links": [
            {"rel": _NODEINFO_SCHEMA_2_1},
        ]
    }

    with respx.mock:
        respx.get(f"{base_url}/.well-known/nodeinfo").mock(return_value=httpx.Response(200, json=jrd))
        with pytest.raises(ValueError, match="missing 'href' field"):
            await NodeInfo.afetch(base_url)


@pytest.mark.asyncio
async def test_afetch_jrd_http_error_raises() -> None:
    base_url = "https://mastodon.example"

    with respx.mock:
        respx.get(f"{base_url}/.well-known/nodeinfo").mock(return_value=httpx.Response(500))
        with pytest.raises(httpx.HTTPStatusError):
            await NodeInfo.afetch(base_url)
