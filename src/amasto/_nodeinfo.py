from __future__ import annotations

from enum import StrEnum
from httpx import AsyncClient, Client, Response
from pydantic import BaseModel
from typing import Any, Final

__all__: Final = (
    "Inbound",
    "NodeInfo",
    "Outbound",
    "Protocol",
    "Services",
    "Software",
    "Usage",
    "Users",
)

_NODEINFO_SCHEMA_2_0 = "http://nodeinfo.diaspora.software/ns/schema/2.0"
_NODEINFO_SCHEMA_2_1 = "http://nodeinfo.diaspora.software/ns/schema/2.1"

_NODEINFO_SCHEMATA: Final = [
    _NODEINFO_SCHEMA_2_0,
    _NODEINFO_SCHEMA_2_1,
]


class NodeInfo(BaseModel):
    version: str
    software: Software
    protocols: list[Protocol]
    services: Services
    openRegistrations: bool
    usage: Usage
    metadata: dict[str, Any]

    @property
    def open_registrations(
        self,
        /,
    ) -> bool:
        return self.openRegistrations

    @staticmethod
    def _nodeinfo_url(jrd_response: Response) -> str:
        jrd_response.raise_for_status()
        jrd = jrd_response.json()
        jrd_links = jrd.get("links", [])
        latest_link: Any = None
        for link in jrd_links:
            link_rel = link.get("rel")
            if link_rel in _NODEINFO_SCHEMATA:
                if latest_link is None or _NODEINFO_SCHEMATA.index(link_rel) > _NODEINFO_SCHEMATA.index(
                    latest_link["rel"]
                ):
                    latest_link = link
        if latest_link is None:
            raise ValueError("No supported NodeInfo schema found in JRD links")
        nodeinfo_url = latest_link.get("href")
        if nodeinfo_url is None:
            raise ValueError("NodeInfo link is missing 'href' field")
        return nodeinfo_url

    @classmethod
    async def afetch(
        cls,
        base_url: str,
        /,
    ) -> NodeInfo:
        async with AsyncClient() as client:
            jrd_response = await client.get(f"{base_url}/.well-known/nodeinfo")
            nodeinfo_response = await client.get(cls._nodeinfo_url(jrd_response=jrd_response))
            nodeinfo_response.raise_for_status()
            nodeinfo = nodeinfo_response.json()
            return cls.model_validate(nodeinfo)

    @classmethod
    def fetch(
        cls,
        base_url: str,
        /,
    ) -> NodeInfo:
        with Client() as client:
            jrd_response = client.get(f"{base_url}/.well-known/nodeinfo")
            nodeinfo_response = client.get(cls._nodeinfo_url(jrd_response=jrd_response))
            nodeinfo_response.raise_for_status()
            nodeinfo = nodeinfo_response.json()
            return cls.model_validate(nodeinfo)


class Software(BaseModel):
    name: str
    version: str


class Protocol(StrEnum):
    ACTIVITYPUB = "activitypub"
    BUDDYCLOUD = "buddycloud"
    DFRN = "dfrn"
    DIASPORA = "diaspora"
    LIBERTREE = "libertree"
    OSTATUS = "ostatus"
    PUMPIO = "pumpio"
    TENT = "tent"
    XMPP = "xmpp"
    ZOT = "zot"


class Services(BaseModel):
    inbound: list[Inbound]
    outbound: list[Outbound]


class Usage(BaseModel):
    users: Users
    localPosts: int | None = None
    localComments: int | None = None

    @property
    def local_posts(
        self,
        /,
    ) -> int | None:
        return self.localPosts

    @property
    def local_comments(
        self,
        /,
    ) -> int | None:
        return self.localComments


class Inbound(StrEnum):
    ATOM1_0 = "atom1.0"
    GNUSOCIAL = "gnusocial"
    IMAP = "imap"
    PNUT = "pnut"
    POP3 = "pop3"
    PUMPIO = "pumpio"
    RSS2_0 = "rss2.0"
    TWITTER = "twitter"


class Outbound(StrEnum):
    ATOM1_0 = "atom1.0"
    BLOGGER = "blogger"
    BUDDYCLOUD = "buddycloud"
    DIASPORA = "diaspora"
    DREAMWIDTH = "dreamwidth"
    DRUPAL = "drupal"
    FACEBOOK = "facebook"
    FRIENDICA = "friendica"
    GNUSOCIAL = "gnusocial"
    GOOGLE = "google"
    INSANEJOURNAL = "insanejournal"
    LIBERTREE = "libertree"
    LINKEDIN = "linkedin"
    LIVEJOURNAL = "livejournal"
    MEDIAGOBLIN = "mediagoblin"
    MYSPACE = "myspace"
    PINTEREST = "pinterest"
    PNUT = "pnut"
    POSTEROUS = "posterous"
    PUMPIO = "pumpio"
    REDMATRIX = "redmatrix"
    RSS2_0 = "rss2.0"
    SMTP = "smtp"
    TENT = "tent"
    TUMBLR = "tumblr"
    TWITTER = "twitter"
    WORDPRESS = "wordpress"
    XMPP = "xmpp"


class Users(BaseModel):
    total: int | None = None
    activeHalfyear: int | None = None
    activeMonth: int | None = None

    @property
    def active_halfyear(
        self,
        /,
    ) -> int | None:
        return self.activeHalfyear

    @property
    def active_month(
        self,
        /,
    ) -> int | None:
        return self.activeMonth
