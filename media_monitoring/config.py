import os

from media_monitoring.providers import (
    FontankaProvider,
    InterfaxProvider,
    IzvestiyaProvider,
    KommersantProvider,
    LentaruProvider,
    MBHProvider,
    MediazonaProvider,
    MeduzaProvider,
    RBKProvider,
    RiaProvider,
    RussianRTProvider,
    TVRainProvider,
    VedomostiProvider,
)

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

PROVIDERS = (
    FontankaProvider,
    InterfaxProvider,
    IzvestiyaProvider,
    KommersantProvider,
    LentaruProvider,
    MBHProvider,
    MediazonaProvider,
    MeduzaProvider,
    RBKProvider,
    RiaProvider,
    RussianRTProvider,
    TVRainProvider,
    VedomostiProvider,
)

MEDIA_INFO = [provider.get_info() for provider in PROVIDERS]
