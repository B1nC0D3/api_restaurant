import json

import redis.asyncio as redis

from apiv1.models.dish import DishResponse
from database.db_operations.abstract_models import AbstractCache
from settings import settings


class DishCache(AbstractCache):
    def __init__(self):
        self.redis = redis.from_url(settings.redis_path, db=2)

    async def get(self, dish_id: int) -> DishResponse | None:
        hashed_dish = await self.redis.get(dish_id)
        if not hashed_dish:
            return None
        dish = json.loads(hashed_dish)
        return DishResponse.parse_obj(dish)

    async def set(
        self, dish_id: int, dish_data: DishResponse,
        expiration: int = 60 * 60,
    ):
        hashed_dish = json.dumps(dish_data.dict())
        await self.redis.set(dish_id, hashed_dish, ex=expiration)

    async def delete(self, dish_id: int) -> None:
        await self.redis.delete(dish_id)

    async def close(self) -> None:
        await self.redis.close()
