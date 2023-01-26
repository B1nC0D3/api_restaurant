from fastapi import HTTPException, status
from sqlalchemy import select

from apiv1.models.menu import DishCreate, DishUpdate
from apiv1.services.base import BaseService
from database.tables import Dish, Submenu


class DishService(BaseService):

    async def get(self, submenu_id: int, dish_id: int) -> Dish:
        return await self._get(submenu_id, dish_id)

    async def get_many(self, submenu_id: int) -> list[Dish]:
        dish = await self.session.execute(
                select(Dish)
                .filter(Dish.submenu_id == submenu_id)
        )
        return dish.unique().scalars().all()

    async def create(self, submenu_id: int, dish_data: DishCreate) -> Dish:
        await self._check_submenu_existence(submenu_id)
        dish = Dish(**dish_data.dict(), submenu_id=submenu_id)
        self.session.add(dish)
        await self.session.commit()
        return dish

    async def update(self, submenu_id: int,
                     dish_id: int, dish_data: DishUpdate) -> Dish:
        dish = await self._get(submenu_id, dish_id)
        for key, value in dish_data:
            setattr(dish, key, value)
        await self.session.commit()
        return dish

    async def delete(self, submenu_id: int, dish_id: int) -> None:
        dish = await self._get(submenu_id, dish_id)
        await self.session.delete(dish)
        await self.session.commit()

    async def _get(self, submenu_id: int, dish_id: int) -> Dish | None:
        dish = await self.session.execute(
                select(Dish)
                .filter(Dish.id == dish_id)
                .filter(Dish.submenu_id == submenu_id)
        )
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='dish not found'
            )
        return dish.scalars().first()

    async def _check_submenu_existence(self, submenu_id: int) -> None:
        submenu = await self.session.execute(
                select(Submenu)
                .filter(Submenu.id == submenu_id)
        )
        submenu = submenu.scalars().first()
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='submenu not found')
