from __future__ import annotations

from ..._endpoint import Endpoint, SubscriptableEndpoint
from ..._params import PaginationParams
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
from typing import TypedDict

__all__ = ("accounts", "get_accounts", "post_accounts")


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
# Flat endpoints
# ---------------------------------------------------------------------------


post_accounts: Endpoint[Token, None, _RegisterAccountBody] = Endpoint(
    "POST",
    "/api/v1/accounts",
    Token,
    body=_RegisterAccountBody,
)

get_accounts: SubscriptableEndpoint[list[Account], _GetAccountsParams, None, Account] = SubscriptableEndpoint(
    "GET",
    "/api/v1/accounts",
    list[Account],
    "/api/v1/accounts/{id}",
    Account,
    params=_GetAccountsParams,
)


# ---------------------------------------------------------------------------
# By-ID namespace
# ---------------------------------------------------------------------------


class _AccountsById:
    __slots__ = (
        "get_endorsements",
        "get_featured_tags",
        "get_followers",
        "get_following",
        "get_identity_proofs",
        "get_lists",
        "get_statuses",
        "post_block",
        "post_endorse",
        "post_follow",
        "post_mute",
        "post_note",
        "post_pin",
        "post_remove_from_followers",
        "post_unblock",
        "post_unendorse",
        "post_unfollow",
        "post_unmute",
        "post_unpin",
    )

    def __init__(self, id: str, /) -> None:
        p = f"/api/v1/accounts/{id}"

        self.get_statuses: Endpoint[list[Status], _AccountStatusesParams, None] = Endpoint(
            "GET",
            f"{p}/statuses",
            list[Status],
            params=_AccountStatusesParams,
        )
        self.get_followers: Endpoint[list[Account], PaginationParams, None] = Endpoint(
            "GET",
            f"{p}/followers",
            list[Account],
            params=PaginationParams,
        )
        self.get_following: Endpoint[list[Account], PaginationParams, None] = Endpoint(
            "GET",
            f"{p}/following",
            list[Account],
            params=PaginationParams,
        )
        self.get_featured_tags: Endpoint[list[FeaturedTag], None, None] = Endpoint(
            "GET",
            f"{p}/featured_tags",
            list[FeaturedTag],
            requires="3.3.0",
        )
        self.get_lists: Endpoint[list[List], None, None] = Endpoint(
            "GET",
            f"{p}/lists",
            list[List],
            requires="2.1.0",
        )
        self.get_endorsements: Endpoint[list[Account], PaginationParams, None] = Endpoint(
            "GET",
            f"{p}/endorsements",
            list[Account],
            params=PaginationParams,
        )
        self.get_identity_proofs: Endpoint[list[IdentityProof], None, None] = Endpoint(
            "GET",
            f"{p}/identity_proofs",
            list[IdentityProof],
            requires="2.8.0",
        )

        self.post_follow: Endpoint[Relationship, None, _FollowBody] = Endpoint(
            "POST",
            f"{p}/follow",
            Relationship,
            body=_FollowBody,
        )
        self.post_unfollow = Endpoint("POST", f"{p}/unfollow", Relationship)
        self.post_remove_from_followers = Endpoint("POST", f"{p}/remove_from_followers", Relationship, requires="3.5.0")
        self.post_block = Endpoint("POST", f"{p}/block", Relationship)
        self.post_unblock = Endpoint("POST", f"{p}/unblock", Relationship)
        self.post_mute: Endpoint[Relationship, None, _MuteBody] = Endpoint(
            "POST",
            f"{p}/mute",
            Relationship,
            body=_MuteBody,
            requires="2.1.0",
        )
        self.post_unmute = Endpoint("POST", f"{p}/unmute", Relationship, requires="2.1.0")
        self.post_pin = Endpoint("POST", f"{p}/pin", Relationship, requires="2.5.0")
        self.post_unpin = Endpoint("POST", f"{p}/unpin", Relationship, requires="2.5.0")
        self.post_endorse = Endpoint("POST", f"{p}/endorse", Relationship, requires="4.4.0")
        self.post_unendorse = Endpoint("POST", f"{p}/unendorse", Relationship, requires="4.4.0")
        self.post_note: Endpoint[Relationship, None, _NoteBody] = Endpoint(
            "POST",
            f"{p}/note",
            Relationship,
            body=_NoteBody,
            requires="4.5.0",
        )


# ---------------------------------------------------------------------------
# Namespace
# ---------------------------------------------------------------------------


class _AccountsNamespace:
    __slots__ = ()

    get_verify_credentials = Endpoint(
        "GET",
        "/api/v1/accounts/verify_credentials",
        CredentialAccount,
    )
    patch_update_credentials: Endpoint[CredentialAccount, None, _UpdateCredentialsBody] = Endpoint(
        "PATCH",
        "/api/v1/accounts/update_credentials",
        CredentialAccount,
        body=_UpdateCredentialsBody,
    )
    get_relationships: Endpoint[list[Relationship], _RelationshipsParams, None] = Endpoint(
        "GET",
        "/api/v1/accounts/relationships",
        list[Relationship],
        params=_RelationshipsParams,
    )
    get_familiar_followers: Endpoint[list[FamiliarFollowers], _FamiliarFollowersParams, None] = Endpoint(
        "GET",
        "/api/v1/accounts/familiar_followers",
        list[FamiliarFollowers],
        params=_FamiliarFollowersParams,
        requires="3.5.0",
    )
    get_search: Endpoint[list[Account], _AccountSearchParams, None] = Endpoint(
        "GET",
        "/api/v1/accounts/search",
        list[Account],
        params=_AccountSearchParams,
    )
    get_lookup: Endpoint[Account, _LookupParams, None] = Endpoint(
        "GET",
        "/api/v1/accounts/lookup",
        Account,
        params=_LookupParams,
        requires="3.4.1",
    )

    def __getitem__(self, id: str) -> _AccountsById:
        return _AccountsById(id)


accounts = _AccountsNamespace()
