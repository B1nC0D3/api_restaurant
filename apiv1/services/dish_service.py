from fastapi import Depends, HTTPException, status

from apiv1.models.dish import DishCreate, DishResponse, DishUpdate
from database.db_operations import dish_cache, menu_cache, submenu_cache
from database.db_operations.dish_operations import DishOperations
from database.tables import Dish


class DishService:
    def __init__(
        self,
        operations: DishOperations = Depends(),
        m_cache: menu_cache.MenuCache = Depends(),
        s_cache: submenu_cache.SubmenuCache = Depends(),
        d_cache: dish_cache.DishCache = Depends(),
    ):
        self.operations = operations
        self.menu_cache = m_cache
        self.submenu_cache = s_cache
        self.dish_cache = d_cache

    async def get_dish(
        self, menu_id: int, submenu_id: int, dish_id: int
    ) -> DishResponse:
        cache = await self.dish_cache.get(dish_id)
        if cache:
            return cache
        dish = await self.operations.get(submenu_id, dish_id)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )
        dish = DishResponse.from_orm(dish)
        await self.dish_cache.set(dish_id, dish)
        return dish

    async def get_dishes(self, menu_id: int, submenu_id: int) -> list[Dish | None]:
        return await self.operations.get_many(submenu_id)

    async def create_dish(
        self, menu_id: int, submenu_id: int, dish_data: DishCreate
    ) -> DishResponse:
        dish = await self.operations.create(submenu_id, dish_data)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )
        parsed_dish = DishResponse.from_orm(dish)
        await self.dish_cache.set(int(dish.id), parsed_dish)
        await self.menu_cache.set_dishes_count(menu_id, "add")
        await self.submenu_cache.set_dishes_count(submenu_id, "add")
        return parsed_dish

    async def update_dish(
        self,
        menu_id: int,
        submenu_id: int,
        dish_id: int,
        dish_data: DishUpdate,
    ) -> DishResponse:
        dish = await self.operations.update(submenu_id, dish_id, dish_data)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )
        dish = DishResponse.from_orm(dish)
        await self.dish_cache.set(dish_id, dish)
        return dish

    async def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int) -> None:
        await self.operations.delete(submenu_id, dish_id)
        await self.dish_cache.delete(dish_id)
        await self.menu_cache.set_dishes_count(menu_id, "delete")
        await self.submenu_cache.set_dishes_count(submenu_id, "delete")
