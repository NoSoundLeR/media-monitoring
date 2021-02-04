import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Tuple

from httpx import AsyncClient, TimeoutException


class Provider:
    id: int
    name: str

    def __init__(self, client: AsyncClient, last_update: datetime) -> None:
        self._client = client
        self._last_update = last_update

    @classmethod
    def get_info(cls) -> Tuple:
        return cls.id, cls.name

    @staticmethod
    def parse_pub_date(s: str):
        return datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %z").astimezone(
            tz=timezone.utc
        )

    @staticmethod
    def parse_link(s: str) -> str:
        return s

    def _parse(self, text: str):
        root = ET.ElementTree(ET.fromstring(text)).getroot()

        ch = root.find("channel")
        news = []
        for item in ch.findall("item"):
            news_date = self.parse_pub_date(item.findtext("pubDate"))
            if news_date > self._last_update:
                res = {}
                title = item.findtext("title")
                res.update({"title": title})

                link = self.parse_link(item.findtext("link"))
                res.update({"link": link})
                res.update({"guid": item.findtext("guid")})
                res.update({"date": news_date})
                news.append(res)
            else:
                break
        return news

    async def poll(self) -> Tuple[str, dict]:
        try:
            res = await self._client.get(self._url, timeout=30)
        except TimeoutException:
            return (
                self.id,
                self.name,
                [],
            )

        if res.status_code == 200:
            return self.id, self.name, self._parse(res.text)
        else:
            return self.id, self.name, []
