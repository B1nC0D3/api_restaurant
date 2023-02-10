from fastapi import HTTPException, status
from sqlalchemy import select

from apiv1.models.menu import DishCreate, DishUpdate
from apiv1.services.base import BaseService
from database.tables import Dish, Submenu, Menu


class DishService(BaseService):

    async def get(self, submenu_id: int, dish_id: int) -> Dish:
        return await self._get(submenu_id, dish_id)

    async def get_many(self, menu_id: int, submenu_id: int, user_id: int) -> list[Dish]:
        dish = await self.session.execute(
                select(Dish)
                .filter(Dish.submenu_id == submenu_id)
        )
        dish = dish.unique().scalars().all()
        if dish:
            await self._is_author(menu_id, user_id)
        return dish

    async def create(self, menu_id: int, submenu_id: int, user_id: int,
                     dish_data: DishCreate) -> Dish:
        await self._check_submenu_existence(submenu_id)
        await self._is_author(menu_id, user_id)
        dish = Dish(**dish_data.dict(), submenu_id=submenu_id)
        self.session.add(dish)
        await self.session.commit()
        return dish

    async def update(self, menu_id: int, submenu_id: int,
                     dish_id: int, user_id: int, dish_data: DishUpdate) -> Dish:
        dish = await self._get(submenu_id, dish_id)
        await self._is_author(menu_id, user_id)
        for key, value in dish_data:
            setattr(dish, key, value)
        await self.session.commit()
        return dish

    async def delete(self, menu_id: int, submenu_id: int, dish_id: int, user_id: int) -> None:
        dish = await self._get(submenu_id, dish_id)
        await self._is_author(menu_id, user_id)
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

    async def _check_menu_existence(self, menu_id: int) -> Menu:
        menu = await self.session.execute(
                select(Menu)
                .filter(Menu.id == menu_id))
        menu = menu.scalars().first()
        if not menu:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Menu not found')
        return menu

    async def _check_submenu_existence(self, submenu_id: int) -> None:
        submenu = await self.session.execute(
                select(Submenu)
                .filter(Submenu.id == submenu_id)
        )
        submenu = submenu.scalars().first()
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='submenu not found')

    async def _is_author(self, menu_id: int, user_id: int):
        menu = await self._check_menu_existence(menu_id)

        if menu.user_id != user_id:
            raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='You are not the author')
