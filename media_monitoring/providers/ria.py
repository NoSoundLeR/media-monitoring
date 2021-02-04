from .base import Provider


class RiaProvider(Provider):
    _url = "https://ria.ru/export/rss2/archive/index.xml"
    id = 5
    name = "RIA Новости"
