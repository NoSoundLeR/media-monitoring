import xml.etree.ElementTree as ET
from datetime import datetime, timezone


from .base import Provider


class RussianRTProvider(Provider):
    _url = "https://russian.rt.com/rss"
    _name = "RT на русском"

    @staticmethod
    def parse_link(s: str) -> str:
        return s.split("?", 1)[0]
