from fastapi import Depends
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apiv1.models.dish import DishCreate, DishUpdate
from database.database import get_session
from database.db_operations.abstract_models import AbstractOperations
from database.tables import Dish, Submenu


class DishOperations(AbstractOperations):
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get(self, submenu_id: int, dish_id: int) -> Dish:
        async with self.session.begin():
            dish = await self.session.execute(
                select(Dish)
                .filter(Dish.submenu_id == submenu_id)
                .filter(Dish.id == dish_id),
            )
        return dish.scalars().first()

    async def get_many(self, submenu_id: int) -> list[Dish | None]:
        async with self.session.begin():
            dishes = await self.session.execute(
                select(Dish).filter(Dish.submenu_id == submenu_id),
            )
        return dishes.unique().scalars().all()

    async def create(self, submenu_id: int, dish_data: DishCreate) -> Dish | None:
        if not await self._check_submenu_existence(submenu_id):
            return None
        async with self.session.begin():
            dish = await self.session.execute(
                insert(Dish)
                .values(submenu_id=submenu_id, **dish_data.dict())
                .returning(Dish),
            )
        return dish.first()

    async def update(
        self,
        submenu_id: int,
        dish_id: int,
        dish_data: DishUpdate,
    ) -> Dish:
        async with self.session.begin():
            dish = await self.session.execute(
                update(Dish)
                .where(Dish.submenu_id == submenu_id)
                .where(Dish.id == dish_id)
                .values(**dish_data.dict())
                .returning(Dish),
            )
        return dish.first()

    async def delete(self, submenu_id: int, dish_id: int) -> None:
        async with self.session.begin():
            await self.session.execute(
                delete(Dish)
                .where(Dish.submenu_id == submenu_id)
                .where(Dish.id == dish_id),
            )

    async def _check_submenu_existence(self, submenu_id: int) -> Submenu | None:
        async with self.session.begin():
            submenu = await self.session.execute(
                select(Submenu).where(Submenu.id == submenu_id),
            )
        return submenu.scalars().first()
