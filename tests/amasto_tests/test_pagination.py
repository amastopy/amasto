from __future__ import annotations

from amasto import Amasto
from amasto._pagination import _parse_next_link
import httpx
import pytest
import respx
from semver import Version

# ---------------------------------------------------------------------------
# _parse_next_link() unit tests
# ---------------------------------------------------------------------------


class TestParseNextLink:
    def test_standard_next_link(self) -> None:
        header = '<https://mastodon.social/api/v1/timelines/home?max_id=123>; rel="next", <https://mastodon.social/api/v1/timelines/home?since_id=456>; rel="prev"'
        assert _parse_next_link(header) == "/api/v1/timelines/home?max_id=123"

    def test_next_only(self) -> None:
        header = '<https://mastodon.social/api/v1/favourites?max_id=789>; rel="next"'
        assert _parse_next_link(header) == "/api/v1/favourites?max_id=789"

    def test_prev_only(self) -> None:
        header = '<https://mastodon.social/api/v1/timelines/home?since_id=456>; rel="prev"'
        assert _parse_next_link(header) is None

    def test_none_header(self) -> None:
        assert _parse_next_link(None) is None

    def test_empty_header(self) -> None:
        assert _parse_next_link("") is None

    def test_malformed_header(self) -> None:
        assert _parse_next_link("not a link header") is None

    def test_path_without_query(self) -> None:
        header = '<https://mastodon.social/api/v1/blocks>; rel="next"'
        assert _parse_next_link(header) == "/api/v1/blocks"

    def test_extracts_path_only(self) -> None:
        """Ensures we never return the full URL (security: no external host following)."""
        header = '<https://evil.example.com/api/v1/timelines/home?max_id=1>; rel="next"'
        result = _parse_next_link(header)
        assert result is not None
        assert not result.startswith("http")
        assert result == "/api/v1/timelines/home?max_id=1"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_client(base_url: str = "https://mastodon.social") -> Amasto:
    """Create an Amasto client with version pre-set (skips NodeInfo discovery)."""
    return Amasto(base_url, "test-token", mastodon_version=Version(4, 3, 0))


def _status_json(id: str) -> dict:
    """Minimal Status-shaped JSON that passes Pydantic validation."""
    return {
        "id": id,
        "created_at": "2025-01-01T00:00:00.000Z",
        "in_reply_to_id": None,
        "in_reply_to_account_id": None,
        "sensitive": False,
        "spoiler_text": "",
        "visibility": "public",
        "language": "en",
        "uri": f"https://mastodon.social/users/alice/statuses/{id}",
        "url": f"https://mastodon.social/@alice/{id}",
        "replies_count": 0,
        "reblogs_count": 0,
        "favourites_count": 0,
        "content": f"<p>Status {id}</p>",
        "reblog": None,
        "application": None,
        "account": {
            "id": "1",
            "username": "alice",
            "acct": "alice",
            "display_name": "Alice",
            "locked": False,
            "bot": False,
            "created_at": "2025-01-01T00:00:00.000Z",
            "note": "",
            "url": "https://mastodon.social/@alice",
            "uri": "https://mastodon.social/users/alice",
            "avatar": "https://mastodon.social/avatars/original/missing.png",
            "avatar_static": "https://mastodon.social/avatars/original/missing.png",
            "header": "https://mastodon.social/headers/original/missing.png",
            "header_static": "https://mastodon.social/headers/original/missing.png",
            "followers_count": 0,
            "following_count": 0,
            "statuses_count": 0,
            "last_status_at": None,
            "emojis": [],
            "fields": [],
        },
        "media_attachments": [],
        "mentions": [],
        "tags": [],
        "emojis": [],
        "card": None,
        "poll": None,
    }


# ---------------------------------------------------------------------------
# PaginatedHttpMethod tests
# ---------------------------------------------------------------------------


class TestPaginatedCall:
    """Test that __call__ returns a single page (backwards compatible)."""

    @pytest.mark.asyncio
    async def test_single_page(self) -> None:
        client = _make_client()
        with respx.mock:
            respx.get("https://mastodon.social/api/v1/bookmarks").mock(
                return_value=httpx.Response(200, json=[_status_json("1"), _status_json("2")]),
            )
            result = await client.api.v1.bookmarks.get()
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0].id == "1"


class TestPaginate:
    """Test the .paginate() async iterator."""

    @pytest.mark.asyncio
    async def test_two_pages(self) -> None:
        client = _make_client()
        page1 = [_status_json("1"), _status_json("2")]
        page2 = [_status_json("3")]

        with respx.mock:
            # Specific route first — respx uses first-match resolution.
            respx.get("https://mastodon.social/api/v1/bookmarks?max_id=2").mock(
                return_value=httpx.Response(200, json=page2),
            )
            respx.get("https://mastodon.social/api/v1/bookmarks").mock(
                return_value=httpx.Response(
                    200,
                    json=page1,
                    headers={"link": '<https://mastodon.social/api/v1/bookmarks?max_id=2>; rel="next"'},
                ),
            )

            ids = []
            async for status in client.api.v1.bookmarks.get.paginate():
                ids.append(status.id)

        assert ids == ["1", "2", "3"]

    @pytest.mark.asyncio
    async def test_empty_first_page(self) -> None:
        client = _make_client()
        with respx.mock:
            respx.get("https://mastodon.social/api/v1/bookmarks").mock(
                return_value=httpx.Response(200, json=[]),
            )

            ids = []
            async for status in client.api.v1.bookmarks.get.paginate():
                ids.append(status.id)

        assert ids == []

    @pytest.mark.asyncio
    async def test_max_items(self) -> None:
        client = _make_client()
        page1 = [_status_json("1"), _status_json("2"), _status_json("3")]

        with respx.mock:
            respx.get("https://mastodon.social/api/v1/bookmarks").mock(
                return_value=httpx.Response(
                    200,
                    json=page1,
                    headers={"link": '<https://mastodon.social/api/v1/bookmarks?max_id=3>; rel="next"'},
                ),
            )

            ids = []
            async for status in client.api.v1.bookmarks.get.paginate(max_items=2):
                ids.append(status.id)

        assert ids == ["1", "2"]

    @pytest.mark.asyncio
    async def test_params_only_first_request(self) -> None:
        """User-supplied params should only be sent on the first request."""
        client = _make_client()

        with respx.mock:
            # Specific routes first.
            route2 = respx.get("https://mastodon.social/api/v1/bookmarks?max_id=1").mock(
                return_value=httpx.Response(200, json=[_status_json("2")]),
            )
            route1 = respx.get("https://mastodon.social/api/v1/bookmarks", params={"limit": "5"}).mock(
                return_value=httpx.Response(
                    200,
                    json=[_status_json("1")],
                    headers={"link": '<https://mastodon.social/api/v1/bookmarks?max_id=1>; rel="next"'},
                ),
            )

            ids = []
            async for status in client.api.v1.bookmarks.get.paginate(params={"limit": 5}):
                ids.append(status.id)

        assert ids == ["1", "2"]
        assert route1.call_count == 1
        assert route2.call_count == 1

    @pytest.mark.asyncio
    async def test_three_pages(self) -> None:
        client = _make_client()

        with respx.mock:
            # Specific routes first.
            respx.get("https://mastodon.social/api/v1/bookmarks?max_id=2").mock(
                return_value=httpx.Response(200, json=[_status_json("3")]),
            )
            respx.get("https://mastodon.social/api/v1/bookmarks?max_id=1").mock(
                return_value=httpx.Response(
                    200,
                    json=[_status_json("2")],
                    headers={"link": '<https://mastodon.social/api/v1/bookmarks?max_id=2>; rel="next"'},
                ),
            )
            respx.get("https://mastodon.social/api/v1/bookmarks").mock(
                return_value=httpx.Response(
                    200,
                    json=[_status_json("1")],
                    headers={"link": '<https://mastodon.social/api/v1/bookmarks?max_id=1>; rel="next"'},
                ),
            )

            ids = []
            async for status in client.api.v1.bookmarks.get.paginate():
                ids.append(status.id)

        assert ids == ["1", "2", "3"]

    @pytest.mark.asyncio
    async def test_max_items_across_pages(self) -> None:
        """max_items should stop mid-page if needed."""
        client = _make_client()

        with respx.mock:
            # Specific route first.
            respx.get("https://mastodon.social/api/v1/bookmarks?max_id=2").mock(
                return_value=httpx.Response(
                    200,
                    json=[_status_json("3"), _status_json("4")],
                ),
            )
            respx.get("https://mastodon.social/api/v1/bookmarks").mock(
                return_value=httpx.Response(
                    200,
                    json=[_status_json("1"), _status_json("2")],
                    headers={"link": '<https://mastodon.social/api/v1/bookmarks?max_id=2>; rel="next"'},
                ),
            )

            ids = []
            async for status in client.api.v1.bookmarks.get.paginate(max_items=3):
                ids.append(status.id)

        assert ids == ["1", "2", "3"]


class TestParse:
    """Test the .parse() convenience method."""

    def test_parse_list(self) -> None:
        client = _make_client()
        result = client.api.v1.bookmarks.get.parse([_status_json("1")])
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].id == "1"
