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

MEDIA_INFO = (
    FontankaProvider.get_info(),
    InterfaxProvider.get_info(),
    IzvestiyaProvider.get_info(),
    KommersantProvider.get_info(),
    LentaruProvider.get_info(),
    MBHProvider.get_info(),
    MediazonaProvider.get_info(),
    MeduzaProvider.get_info(),
    RBKProvider.get_info(),
    RiaProvider.get_info(),
    RussianRTProvider.get_info(),
    TVRainProvider.get_info(),
    VedomostiProvider.get_info(),
)
