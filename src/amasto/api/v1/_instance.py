from __future__ import annotations

from ..._endpoint import Endpoint, EndpointTemplate
from ...models.v1 import (
    DomainBlock,
    ExtendedDescription,
    Instance,
    PrivacyPolicy,
    Rule,
    TermsOfService,
)

__all__ = ("get_instance", "instance")


get_instance = Endpoint("GET", "/api/v1/instance", Instance, requires="1.0.0")


class _InstanceNamespace:
    __slots__ = ()

    get_peers: Endpoint[list[str], None, None] = Endpoint(
        "GET",
        "/api/v1/instance/peers",
        list[str],
        requires="1.1.0",
    )
    get_activity: Endpoint[list[dict], None, None] = Endpoint(
        "GET",
        "/api/v1/instance/activity",
        list[dict],
        requires="2.1.2",
    )
    get_rules: Endpoint[list[Rule], None, None] = Endpoint(
        "GET",
        "/api/v1/instance/rules",
        list[Rule],
        requires="2.4.0",
    )
    get_domain_blocks: Endpoint[list[DomainBlock], None, None] = Endpoint(
        "GET",
        "/api/v1/instance/domain_blocks",
        list[DomainBlock],
        requires="4.0.0",
    )
    get_extended_description = Endpoint(
        "GET",
        "/api/v1/instance/extended_description",
        ExtendedDescription,
    )
    get_privacy_policy = Endpoint(
        "GET",
        "/api/v1/instance/privacy_policy",
        PrivacyPolicy,
        requires="4.0.0",
    )
    get_terms_of_service = Endpoint(
        "GET",
        "/api/v1/instance/terms_of_service",
        TermsOfService,
        requires="4.4.0",
    )
    get_terms_of_service_by_date: EndpointTemplate[TermsOfService, None, None] = EndpointTemplate(
        "GET",
        "/api/v1/instance/terms_of_service/{date}",
        TermsOfService,
        requires="4.4.0",
    )
    get_translation_languages: Endpoint[dict[str, list[str]], None, None] = Endpoint(
        "GET",
        "/api/v1/instance/translation_languages",
        dict[str, list[str]],
        requires="4.0.0",
    )


instance = _InstanceNamespace()
