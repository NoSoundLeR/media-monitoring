from .base import Provider


class LentaruProvider(Provider):
    _url = "https://lenta.ru/rss"
    id = 8
    name = "Lenta.ru"
