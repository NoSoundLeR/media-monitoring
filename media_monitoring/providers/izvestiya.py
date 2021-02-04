from .base import Provider


class IzvestiyaProvider(Provider):
    _url = "https://iz.ru/xml/rss/all.xml"
    name = "Известия"
    id = 3
