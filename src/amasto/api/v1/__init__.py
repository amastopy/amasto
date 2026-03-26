from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import Amasto

__all__ = ("V1Namespace",)


class V1Namespace:
    __slots__ = (
        "accounts",
        "announcements",
        "apps",
        "blocks",
        "bookmarks",
        "conversations",
        "custom_emojis",
        "directory",
        "domain_blocks",
        "emails",
        "endorsements",
        "favourites",
        "featured_tags",
        "follow_requests",
        "followed_tags",
        "instance",
        "lists",
        "markers",
        "media",
        "mutes",
        "notifications",
        "polls",
        "preferences",
        "profile",
        "push",
        "reports",
        "scheduled_statuses",
        "search",
        "statuses",
        "streaming",
        "suggestions",
        "tags",
        "timelines",
        "trends",
    )

    def __init__(self, client: Amasto, /) -> None:
        from ._accounts import AccountsResource
        from ._announcements import AnnouncementsResource
        from ._apps import AppsResource
        from ._blocks import BlocksResource
        from ._bookmarks import BookmarksResource
        from ._conversations import ConversationsResource
        from ._custom_emojis import CustomEmojisResource
        from ._directory import DirectoryResource
        from ._domain_blocks import DomainBlocksResource
        from ._emails import EmailsResource
        from ._endorsements import EndorsementsResource
        from ._favourites import FavouritesResource
        from ._featured_tags import FeaturedTagsResource
        from ._follow_requests import FollowRequestsResource
        from ._followed_tags import FollowedTagsResource
        from ._instance import InstanceResource
        from ._lists import ListsResource
        from ._markers import MarkersResource
        from ._media import MediaResource
        from ._mutes import MutesResource
        from ._notifications import NotificationsResource
        from ._polls import PollsResource
        from ._preferences import PreferencesResource
        from ._profile import ProfileResource
        from ._push import PushResource
        from ._reports import ReportsResource
        from ._scheduled_statuses import ScheduledStatusesResource
        from ._search import SearchResource
        from ._statuses import StatusesResource
        from ._streaming import StreamingResource
        from ._suggestions import SuggestionsResource
        from ._tags import TagsResource
        from ._timelines import TimelinesResource
        from ._trends import TrendsResource

        self.accounts = AccountsResource(client)
        self.announcements = AnnouncementsResource(client)
        self.apps = AppsResource(client)
        self.blocks = BlocksResource(client)
        self.bookmarks = BookmarksResource(client)
        self.conversations = ConversationsResource(client)
        self.custom_emojis = CustomEmojisResource(client)
        self.directory = DirectoryResource(client)
        self.domain_blocks = DomainBlocksResource(client)
        self.emails = EmailsResource(client)
        self.endorsements = EndorsementsResource(client)
        self.favourites = FavouritesResource(client)
        self.featured_tags = FeaturedTagsResource(client)
        self.follow_requests = FollowRequestsResource(client)
        self.followed_tags = FollowedTagsResource(client)
        self.instance = InstanceResource(client)
        self.lists = ListsResource(client)
        self.markers = MarkersResource(client)
        self.media = MediaResource(client)
        self.mutes = MutesResource(client)
        self.notifications = NotificationsResource(client)
        self.polls = PollsResource(client)
        self.preferences = PreferencesResource(client)
        self.profile = ProfileResource(client)
        self.push = PushResource(client)
        self.reports = ReportsResource(client)
        self.scheduled_statuses = ScheduledStatusesResource(client)
        self.search = SearchResource(client)
        self.statuses = StatusesResource(client)
        self.streaming = StreamingResource(client)
        self.suggestions = SuggestionsResource(client)
        self.tags = TagsResource(client)
        self.timelines = TimelinesResource(client)
        self.trends = TrendsResource(client)
