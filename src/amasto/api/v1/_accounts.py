from __future__ import annotations

from ..._params import PaginationParams
from ..._resource import HttpMethod
from ...models.v1 import (
    Account,
    CredentialAccount,
    FamiliarFollowers,
    FeaturedTag,
    IdentityProof,
    List,
    Relationship,
    Status,
    Token,
)
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("AccountsResource",)


# ---------------------------------------------------------------------------
# TypedDicts
# ---------------------------------------------------------------------------


class _RegisterAccountBody(TypedDict, total=False):
    username: str
    email: str
    password: str
    agreement: bool
    locale: str
    reason: str
    date_of_birth: str


class _GetAccountsParams(TypedDict):
    id: list[str]


class _UpdateCredentialsBody(TypedDict, total=False):
    display_name: str
    note: str
    locked: bool
    bot: bool
    discoverable: bool
    hide_collections: bool
    indexable: bool
    attribution_domains: list[str]


class _AccountStatusesParams(TypedDict, total=False):
    max_id: str
    since_id: str
    min_id: str
    limit: int
    only_media: bool
    exclude_replies: bool
    exclude_reblogs: bool
    pinned: bool
    tagged: str


class _FollowBody(TypedDict, total=False):
    reblogs: bool
    notify: bool
    languages: list[str]


class _MuteBody(TypedDict, total=False):
    notifications: bool
    duration: int


class _NoteBody(TypedDict, total=False):
    comment: str


class _RelationshipsParams(TypedDict, total=False):
    id: list[str]
    with_suspended: bool


class _FamiliarFollowersParams(TypedDict):
    id: list[str]


class _AccountSearchParams(TypedDict, total=False):
    q: str
    limit: int
    offset: int
    resolve: bool
    following: bool


class _LookupParams(TypedDict):
    acct: str


# ---------------------------------------------------------------------------
# Sub-resources for by-ID
# ---------------------------------------------------------------------------


class _StatusesSubResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[list[Status], _AccountStatusesParams, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/accounts/{id}/statuses",
            list[Status],
        )


class _FollowersResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[list[Account], PaginationParams, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/accounts/{id}/followers",
            list[Account],
        )


class _FollowingResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[list[Account], PaginationParams, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/accounts/{id}/following",
            list[Account],
        )


class _AccountFeaturedTagsResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[list[FeaturedTag], None, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/accounts/{id}/featured_tags",
            list[FeaturedTag],
            requires="3.3.0",
        )


class _AccountListsResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[list[List], None, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/accounts/{id}/lists",
            list[List],
            requires="2.1.0",
        )


class _AccountEndorsementsResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[list[Account], PaginationParams, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/accounts/{id}/endorsements",
            list[Account],
        )


class _IdentityProofsResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[list[IdentityProof], None, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/accounts/{id}/identity_proofs",
            list[IdentityProof],
            requires="2.8.0",
        )


class _FollowActionResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Relationship, None, _FollowBody] = HttpMethod(
            client,
            "POST",
            f"/api/v1/accounts/{id}/follow",
            Relationship,
        )


class _UnfollowResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Relationship, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/accounts/{id}/unfollow",
            Relationship,
        )


class _RemoveFromFollowersResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Relationship, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/accounts/{id}/remove_from_followers",
            Relationship,
            requires="3.5.0",
        )


class _BlockActionResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Relationship, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/accounts/{id}/block",
            Relationship,
        )


class _UnblockResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Relationship, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/accounts/{id}/unblock",
            Relationship,
        )


class _MuteActionResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Relationship, None, _MuteBody] = HttpMethod(
            client,
            "POST",
            f"/api/v1/accounts/{id}/mute",
            Relationship,
            requires="2.1.0",
        )


class _UnmuteResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Relationship, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/accounts/{id}/unmute",
            Relationship,
            requires="2.1.0",
        )


class _PinActionResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Relationship, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/accounts/{id}/pin",
            Relationship,
            requires="2.5.0",
        )


class _UnpinResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Relationship, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/accounts/{id}/unpin",
            Relationship,
            requires="2.5.0",
        )


class _EndorseActionResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Relationship, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/accounts/{id}/endorse",
            Relationship,
            requires="4.4.0",
        )


class _UnendorseResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Relationship, None, None] = HttpMethod(
            client,
            "POST",
            f"/api/v1/accounts/{id}/unendorse",
            Relationship,
            requires="4.4.0",
        )


class _NoteActionResource:
    __slots__ = ("post",)

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.post: HttpMethod[Relationship, None, _NoteBody] = HttpMethod(
            client,
            "POST",
            f"/api/v1/accounts/{id}/note",
            Relationship,
            requires="4.5.0",
        )


# ---------------------------------------------------------------------------
# By-ID resource
# ---------------------------------------------------------------------------


class _AccountByIdResource:
    __slots__ = (
        "block",
        "endorse",
        "endorsements",
        "featured_tags",
        "follow",
        "followers",
        "following",
        "get",
        "identity_proofs",
        "lists",
        "mute",
        "note",
        "pin",
        "remove_from_followers",
        "statuses",
        "unblock",
        "unendorse",
        "unfollow",
        "unmute",
        "unpin",
    )

    def __init__(self, client: Amasto, id: str, /) -> None:
        self.get: HttpMethod[Account, None, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/accounts/{id}",
            Account,
        )
        self.statuses = _StatusesSubResource(client, id)
        self.followers = _FollowersResource(client, id)
        self.following = _FollowingResource(client, id)
        self.featured_tags = _AccountFeaturedTagsResource(client, id)
        self.lists = _AccountListsResource(client, id)
        self.endorsements = _AccountEndorsementsResource(client, id)
        self.identity_proofs = _IdentityProofsResource(client, id)
        self.follow = _FollowActionResource(client, id)
        self.unfollow = _UnfollowResource(client, id)
        self.remove_from_followers = _RemoveFromFollowersResource(client, id)
        self.block = _BlockActionResource(client, id)
        self.unblock = _UnblockResource(client, id)
        self.mute = _MuteActionResource(client, id)
        self.unmute = _UnmuteResource(client, id)
        self.pin = _PinActionResource(client, id)
        self.unpin = _UnpinResource(client, id)
        self.endorse = _EndorseActionResource(client, id)
        self.unendorse = _UnendorseResource(client, id)
        self.note = _NoteActionResource(client, id)


# ---------------------------------------------------------------------------
# Sub-resources for top-level
# ---------------------------------------------------------------------------


class _VerifyCredentialsResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[CredentialAccount, None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/accounts/verify_credentials",
            CredentialAccount,
        )


class _UpdateCredentialsResource:
    __slots__ = ("patch",)

    def __init__(self, client: Amasto, /) -> None:
        self.patch: HttpMethod[CredentialAccount, None, _UpdateCredentialsBody] = HttpMethod(
            client,
            "PATCH",
            "/api/v1/accounts/update_credentials",
            CredentialAccount,
        )


class _RelationshipsResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[Relationship], _RelationshipsParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/accounts/relationships",
            list[Relationship],
        )


class _FamiliarFollowersResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[FamiliarFollowers], _FamiliarFollowersParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/accounts/familiar_followers",
            list[FamiliarFollowers],
            requires="3.5.0",
        )


class _AccountSearchResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[Account], _AccountSearchParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/accounts/search",
            list[Account],
        )


class _LookupResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[Account, _LookupParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/accounts/lookup",
            Account,
            requires="3.4.1",
        )


# ---------------------------------------------------------------------------
# Top-level resource
# ---------------------------------------------------------------------------


class AccountsResource:
    __slots__ = (
        "_client",
        "familiar_followers",
        "get",
        "lookup",
        "post",
        "relationships",
        "search",
        "update_credentials",
        "verify_credentials",
    )

    def __init__(self, client: Amasto, /) -> None:
        self._client = client
        self.get: HttpMethod[list[Account], _GetAccountsParams, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/accounts",
            list[Account],
        )
        self.post: HttpMethod[Token, None, _RegisterAccountBody] = HttpMethod(
            client,
            "POST",
            "/api/v1/accounts",
            Token,
        )
        self.verify_credentials = _VerifyCredentialsResource(client)
        self.update_credentials = _UpdateCredentialsResource(client)
        self.relationships = _RelationshipsResource(client)
        self.familiar_followers = _FamiliarFollowersResource(client)
        self.search = _AccountSearchResource(client)
        self.lookup = _LookupResource(client)

    def __getitem__(self, id: str) -> _AccountByIdResource:
        return _AccountByIdResource(self._client, id)
