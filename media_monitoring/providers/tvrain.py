from .base import Provider


class TVRainProvider(Provider):
    _url = "https://tvrain.ru/export/rss/programs/1018.xml"
    id = 7
    name = "Дождь"
