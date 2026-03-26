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
        "_streaming_url",
        "api",
        "health",
        "oauth",
    )

    _base_url: str
    _api_key: str
    _mastodon_version: Version | None
    _initialized: bool
    _http: httpx.AsyncClient
    _streaming_url: str

    def __init__(
        self,
        base_url: str,
        api_key: str,
        /,
        *,
        mastodon_version: Version | None = None,
        streaming_url: str | None = None,
    ) -> None:
        from .api import ApiNamespace
        from .health import HealthResource
        from .oauth import OAuthNamespace

        self._base_url = base_url
        self._api_key = api_key
        self._mastodon_version = None
        self._streaming_url = (
            streaming_url
            if streaming_url is not None
            else base_url.replace("https://", "wss://").replace("http://", "ws://")
        )
        self._http = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        self._initialized = False

        self.api = ApiNamespace(self)
        self.oauth = OAuthNamespace(self)
        self.health = HealthResource(self)

        if mastodon_version is not None and streaming_url is not None:
            self._mastodon_version = mastodon_version
            self._initialized = True
        else:
            self._initialize(
                skip_nodeinfo=mastodon_version is not None,
                skip_instance=streaming_url is not None,
            )
            if mastodon_version is not None:
                self._mastodon_version = mastodon_version

    def _initialize(
        self,
        /,
        *,
        skip_nodeinfo: bool = False,
        skip_instance: bool = False,
    ) -> None:
        if self._initialized:
            return
        if not skip_nodeinfo:
            nodeinfo = NodeInfo.fetch(self._base_url)
            if nodeinfo.software.name == "mastodon":
                self._mastodon_version = Version.parse(nodeinfo.software.version)
        if not skip_instance:
            instance_response = httpx.get(
                f"{self._base_url}/api/v1/instance",
                headers={"Authorization": f"Bearer {self._api_key}"},
            )
            instance_response.raise_for_status()
            data = instance_response.json()
            urls = data.get("urls", {})
            streaming_api = urls.get("streaming_api")
            if streaming_api is not None:
                self._streaming_url = streaming_api
        self._initialized = True
