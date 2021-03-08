import logging
import sys
from typing import List, Optional

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from pymongo.errors import ServerSelectionTimeoutError

from media_monitoring.config import DATABASE_NAME, DATABASE_URL

log = logging.getLogger("media")


class DB:
    def __init__(self):
        self._client = AsyncIOMotorClient(DATABASE_URL)
        try:
            self._client.is_mongos
        except ServerSelectionTimeoutError:
            log.error("Can't connect to db!")
            sys.exit(1)
        self._db = self._client[DATABASE_NAME]

        self._chats = self._db["chats"]

    async def close_connection(self, *args) -> None:
        log.info("Closing connection to db...")
        self._client.close()

    async def run(self, id: int) -> None:
        await self._chats.update_one({"id": id}, {"$set": {"active": True}})

    async def stop(self, id: int) -> None:
        await self._chats.update_one({"id": id}, {"$set": {"active": False}})

    async def get_active_chats(self) -> List[dict]:
        return await self._chats.find(
            {
                "active": {"$eq": True},
                "media": {"$not": {"$size": 0}},
                "targets": {"$not": {"$size": 0}},
            }
        ).to_list(None)

    async def get_chat(self, id: int) -> dict:
        chat = await self._chats.find_one({"id": id})
        if chat is None:
            initial_data = {"id": id, "targets": [], "media": [], "active": False}
            await self._chats.insert_one(initial_data)
            return initial_data
        else:
            return chat

    async def delete_chat(self, id: int) -> None:
        await self._chats.delete_one({"id": id})

    async def get_targets(self, id: int) -> Optional[List]:
        chat = await self.get_chat(id)
        if chat is not None:
            return chat.get("targets")
        return None

    async def update_targets(self, id: int, target: str) -> bool:
        targets = await self.get_targets(id)
        if target in targets:
            targets.remove(target)
        else:
            targets.append(target)
        res = await self._chats.find_one_and_update(
            {"id": id},
            {"$set": {"targets": targets}},
            return_document=ReturnDocument.AFTER,
        )
        return res.get("targets")

    async def get_media(self, id: int) -> Optional[List]:
        chat = await self.get_chat(id)
        if chat is not None:
            return chat.get("media")

    async def update_media(self, id: int, media_id: int) -> List[int]:
        media = await self.get_media(id)
        if media_id in media:
            media.remove(media_id)
        else:
            media.append(media_id)
        res = await self._chats.find_one_and_update(
            {"id": id},
            {"$set": {"media": media}},
            return_document=ReturnDocument.AFTER,
        )
        return res.get("media")


db = DB()
