import xml.etree.ElementTree as ET
from datetime import datetime, timezone


from .base import Provider


class MeduzaProvider(Provider):
    _url = "https://meduza.io/rss2/all"
    _name = "Медуза"

