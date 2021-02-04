from .base import Provider


class VedomostiProvider(Provider):
    _url = "https://www.vedomosti.ru/rss/news"
    id = 11
    name = "Ведомости"
