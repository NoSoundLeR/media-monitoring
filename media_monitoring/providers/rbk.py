from .base import Provider


class RBKProvider(Provider):
    _url = "http://static.feed.rbc.ru/rbc/internal/rss.rbc.ru/rbc.ru/news.rss"
    id = 12
    name = "РБК"
