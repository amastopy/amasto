from __future__ import annotations

from ..._resource import HttpMethod
from ...models.v1 import (
    DomainBlock,
    ExtendedDescription,
    Instance,
    PrivacyPolicy,
    Rule,
    TermsOfService,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("InstanceResource",)


class _PeersResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[str], None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/instance/peers",
            list[str],
            requires="1.1.0",
        )


class _ActivityResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[dict], None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/instance/activity",
            list[dict],
            requires="2.1.2",
        )


class _RulesResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[Rule], None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/instance/rules",
            list[Rule],
            requires="2.4.0",
        )


class _InstanceDomainBlocksResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[list[DomainBlock], None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/instance/domain_blocks",
            list[DomainBlock],
            requires="4.0.0",
        )


class _ExtendedDescriptionResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[ExtendedDescription, None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/instance/extended_description",
            ExtendedDescription,
        )


class _PrivacyPolicyResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[PrivacyPolicy, None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/instance/privacy_policy",
            PrivacyPolicy,
            requires="4.0.0",
        )


class _TermsOfServiceByDateResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, date: str, /) -> None:
        self.get: HttpMethod[TermsOfService, None, None] = HttpMethod(
            client,
            "GET",
            f"/api/v1/instance/terms_of_service/{date}",
            TermsOfService,
            requires="4.4.0",
        )


class _TermsOfServiceResource:
    __slots__ = ("_client", "get")

    def __init__(self, client: Amasto, /) -> None:
        self._client = client
        self.get: HttpMethod[TermsOfService, None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/instance/terms_of_service",
            TermsOfService,
            requires="4.4.0",
        )

    def __getitem__(self, date: str) -> _TermsOfServiceByDateResource:
        return _TermsOfServiceByDateResource(self._client, date)


class _TranslationLanguagesResource:
    __slots__ = ("get",)

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[dict[str, list[str]], None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/instance/translation_languages",
            dict[str, list[str]],
            requires="4.0.0",
        )


class InstanceResource:
    __slots__ = (
        "activity",
        "domain_blocks",
        "extended_description",
        "get",
        "peers",
        "privacy_policy",
        "rules",
        "terms_of_service",
        "translation_languages",
    )

    def __init__(self, client: Amasto, /) -> None:
        self.get: HttpMethod[Instance, None, None] = HttpMethod(
            client,
            "GET",
            "/api/v1/instance",
            Instance,
            requires="1.0.0",
        )
        self.peers = _PeersResource(client)
        self.activity = _ActivityResource(client)
        self.rules = _RulesResource(client)
        self.domain_blocks = _InstanceDomainBlocksResource(client)
        self.extended_description = _ExtendedDescriptionResource(client)
        self.privacy_policy = _PrivacyPolicyResource(client)
        self.terms_of_service = _TermsOfServiceResource(client)
        self.translation_languages = _TranslationLanguagesResource(client)
