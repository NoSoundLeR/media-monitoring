import asyncio
import logging
from datetime import datetime, timedelta, timezone

from httpx import AsyncClient

from media_monitoring.config import PROVIDERS
from media_monitoring.db import db
from media_monitoring.telegram import escape_msg, send_notification

log = logging.getLogger("media")


class Worker:
    def __init__(self) -> None:
        self.i = 0

    def refresh_last_update(self) -> None:
        self.last_update = datetime.utcnow().replace(tzinfo=timezone.utc)
        self.i += 1

    def set_last_update(self, last_update: datetime) -> None:
        self.last_update = last_update


worker = Worker()


def check_words(item, words) -> bool:
    title = item.get("title").lower()
    return any(word.lower() in title for word in words)


async def run_monitoring(offset: int, timeout: int) -> None:
    if offset:
        worker.set_last_update(
            (datetime.utcnow() - timedelta(seconds=offset)).replace(tzinfo=timezone.utc)
        )
    else:
        worker.set_last_update(datetime.utcnow().replace(tzinfo=timezone.utc))
    asyncio.create_task(monitor(timeout))


async def monitor(timeout: int) -> None:
    log.debug(f"i: {worker.i}")
    log.debug(f"last update: {worker.last_update}")
    async with AsyncClient() as client:
        tasks = []
        for provider in [
            provider(client, worker.last_update) for provider in PROVIDERS
        ]:
            tasks.append(provider.poll())

        results = await asyncio.gather(*tasks)
    worker.refresh_last_update()
    active_chats = await db.get_active_chats()
    for id, name, data in results:
        log.debug(f"id: {id}")
        log.debug(f"name: {name}")
        log.debug(data)
        for chat in active_chats:
            if id not in chat.get("media"):
                continue
            for item in data:
                if check_words(item, chat.get("targets")):
                    msg = "\n".join(
                        [
                            f"*{name}*",
                            f"[{escape_msg(item.get('title'))}]({escape_msg(item.get('link'))})",
                        ]
                    )
                    asyncio.create_task(send_notification(chat.get("id"), msg))

    await asyncio.sleep(timeout)
    asyncio.create_task(monitor(timeout))
