from fastapi import HTTPException, status, Depends

from apiv1.models.dish import DishCreate, DishUpdate, DishResponse
from database.db_operations.dishes_operations import DishOperations


class DishService:

    def __init__(self, operations: DishOperations = Depends()):
        self.operations = operations

    async def get_dish(self, submenu_id: int, dish_id: int) -> DishResponse:
        dish = await self.operations.get(submenu_id, dish_id)
        if not dish:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='dish not found')
        return dish

    async def get_dishes(self, submenu_id: int) -> list[DishResponse]:
        return await self.operations.get_many(submenu_id)

    async def create_dish(self, submenu_id: int, dish_data: DishCreate) -> DishResponse:
        dish = await self.operations.create(submenu_id, dish_data)
        if not dish:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='submenu not found')
        return dish

    async def update_dish(self, submenu_id: int,
                          dish_id: int, dish_data: DishUpdate) -> DishResponse:
        dish = await self.operations.update(submenu_id, dish_id, dish_data)
        if not dish:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='submenu not found')
        return dish

    async def delete_dish(self, submenu_id: int, dish_id: int) -> None:
        await self.operations.delete(submenu_id, dish_id)
