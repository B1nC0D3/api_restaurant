import json

import redis.asyncio as redis  # type: ignore

from apiv1.models.submenu import SubmenuResponse
from database.db_operations.abstract_models import AbstractCache
from settings import settings


class SubmenuCache(AbstractCache):
    def __init__(self):
        self.redis = redis.from_url(settings.redis_path, db=1)

    async def get(self, submenu_id: int) -> SubmenuResponse | None:
        hashed_submenu = await self.redis.get(submenu_id)
        if not hashed_submenu:
            return None
        submenu = json.loads(hashed_submenu)
        return SubmenuResponse.parse_obj(submenu)

    async def set(
        self,
        submenu_id: int,
        submenu_data: SubmenuResponse,
        expiration: int = 60 * 60,
    ):
        hashed_submenu = json.dumps(submenu_data.dict())
        await self.redis.set(submenu_id, hashed_submenu, ex=expiration)

    async def delete(self, submenu_id: int) -> None:
        await self.redis.delete(submenu_id)

    async def close(self) -> None:
        await self.redis.close()

    async def set_dishes_count(self, submenu_id: int, action: str):
        submenu = await self.get(submenu_id)
        if not submenu:
            return None
        if action == "add":
            submenu.dishes_count += 1
        else:
            submenu.dishes_count -= 1
        await self.set(submenu_id, submenu)
