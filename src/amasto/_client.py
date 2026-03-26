from __future__ import annotations

from ._nodeinfo import NodeInfo
import httpx
from semver import Version


class Amasto:
    __slots__ = (
        "_api_key",
        "_base_url",
        "_http",
        "_initialized",
        "_mastodon_version",
        "api",
        "health",
        "oauth",
    )

    _base_url: str
    _api_key: str
    _mastodon_version: Version | None
    _initialized: bool
    _http: httpx.AsyncClient

    def __init__(
        self,
        base_url: str,
        api_key: str,
        /,
        *,
        mastodon_version: Version | None = None,
    ) -> None:
        from .api import ApiNamespace
        from .health import HealthResource
        from .oauth import OAuthNamespace

        self._base_url = base_url
        self._api_key = api_key
        self._mastodon_version = None
        self._http = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        self._initialized = False

        self.api = ApiNamespace(self)
        self.oauth = OAuthNamespace(self)
        self.health = HealthResource(self)

        if mastodon_version is not None:
            self._mastodon_version = mastodon_version
            self._initialized = True
        else:
            self._initialize()

    def _initialize(
        self,
        /,
    ) -> None:
        if self._initialized:
            return
        nodeinfo = NodeInfo.fetch(self._base_url)
        if nodeinfo.software.name == "mastodon":
            self._mastodon_version = Version.parse(nodeinfo.software.version)
        self._initialized = True
