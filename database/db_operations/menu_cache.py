import json

import redis.asyncio as redis

from apiv1.models.menu import MenuResponse
from database.db_operations.base import AbstractCache
from settings import settings


class MenuCache(AbstractCache):
    def __init__(self):
        self.redis = redis.from_url(settings.redis_path, db=0)

    async def get(self, menu_id: int) -> MenuResponse | None:
        hashed_menu = await self.redis.get(menu_id)
        if not hashed_menu:
            return None
        menu = json.loads(hashed_menu)
        return MenuResponse.parse_obj(menu)

    async def set(self, menu_id: int, menu_data: MenuResponse,
                  expiration: int = 60*60):
        hashed_menu = json.dumps(menu_data.dict())
        await self.redis.set(menu_id, hashed_menu, ex=expiration)

    async def delete(self, menu_id: int) -> None:
        await self.redis.delete(menu_id)

    async def close(self) -> None:
        await self.redis.close()

    async def set_submenus_count(self, menu_id: int, action: str):
        menu = await self.get(menu_id)
        if action == 'add':
            menu.submenus_count += 1
        else:
            menu.submenus_count -= 1
        await self.set(menu_id, menu)

    async def set_dishes_count(self, menu_id: int, action: str):
        menu = await self.get(menu_id)
        if action == 'add':
            menu.dishes_count += 1
        else:
            menu.dishes_count -= 1
        await self.set(menu_id, menu)
