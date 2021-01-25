import xml.etree.ElementTree as ET
from datetime import datetime, timezone


from .base import Provider


class IzvestiyaProvider(Provider):
    _url = "https://iz.ru/xml/rss/all.xml"
    _name = "Известия"
