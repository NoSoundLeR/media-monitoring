from .base import Provider


class RussianRTProvider(Provider):
    _url = "https://russian.rt.com/rss"
    id = 13
    name = "RT на русском"

    @staticmethod
    def parse_link(s: str) -> str:
        return s.split("?", 1)[0]
