from datetime import datetime, timezone

from .base import Provider


class MediazonaProvider(Provider):
    _url = "https://zona.media/rss"
    id = 1
    name = "Медиазона"

    @staticmethod
    def parse_pub_date(s: str):
        return datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %Z").replace(
            tzinfo=timezone.utc
        )
