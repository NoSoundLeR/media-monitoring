import asyncio
from datetime import datetime, timezone
from httpx import AsyncClient
from typing import Optional

from monitor.providers import (
    RussianRTProvider,
    MediazonaProvider,
    MeduzaProvider,
    IzvestiyaProvider,
)

TIMEOUT = 60 * 5


class Worker:
    def __init__(self, init: Optional[datetime] = None) -> None:
        if init is not None:
            self.last_update = init.replace(tzinfo=timezone.utc)
        else:
            self.last_update = datetime.utcnow().replace(tzinfo=timezone.utc)

        self.i = 1

    def refresh_last_update(self) -> None:
        self.last_update = datetime.utcnow().replace(tzinfo=timezone.utc)
        self.i += 1


worker = Worker()


def check_words(item, words):
    title = item.get("title").lower()
    return any(word.lower() in title for word in words)


async def main(worker):
    print("Executing main...")
    print(worker.last_update)
    print(f"i={worker.i}")
    words = ["Россия"]
    print("Looking for:")
    print(words)
    async with AsyncClient() as client:
        tasks = []
        for provider in [
            provider(client, worker.last_update)
            for provider in (
                RussianRTProvider,
                MediazonaProvider,
                MeduzaProvider,
                IzvestiyaProvider,
            )
        ]:
            tasks.append(provider.poll())

        results = await asyncio.gather(*tasks)
    worker.refresh_last_update()
    for res in results:
        name = res[0]
        data = res[1][1]

        # for user in users:
        for item in data:
            if check_words(item, words):
                print(name)
                print(item.get("title"))
                print("---")

    print("------END------")
    await asyncio.sleep(TIMEOUT)
    asyncio.create_task(main(worker))


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.create_task(main(worker))
    loop.run_forever()
