from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from apiv1.models.menu import MenuCreate, MenuUpdate
from database.tables import Dish, Menu, Submenu
from .base import BaseService


class MenuService(BaseService):

    async def get(self, menu_id: int) -> Menu:
        return await self._get(menu_id)

    async def get_many(self) -> list[Menu]:
        menus = await self.session.execute(select(Menu))
        menus = menus.scalars().all()
        for menu in menus:
            menu.submenus_count = await self._get_submenus_count(menu.id)
            menu.dishes_count = await self._get_dishes_count(menu.id)
        return menus

    async def create(self, menu_data: MenuCreate) -> Menu:
        menu = Menu(
            **menu_data.dict()
        )
        self.session.add(menu)
        await self.session.commit()
        menu.submenus_count = await self._get_submenus_count(menu.id)
        menu.dishes_count = await self._get_dishes_count(menu.id)
        return menu

    async def update(self, menu_id: int, menu_data: MenuUpdate) -> Menu:
        menu = await self._get(menu_id)
        for key, value in menu_data:
            setattr(menu, key, value)
        await self.session.commit()
        return menu

    async def delete(self, menu_id: int) -> None:
        menu = await self._get(menu_id)
        await self.session.delete(menu)
        await self.session.commit()

    async def _get_submenus_count(self, menu_id: int) -> int:
        submenus_count = await self.session.execute(
                select(func.count(Submenu.id))
                .select_from(Menu)
                .join(Menu.submenus)
                .filter(Menu.id == menu_id))
        return submenus_count.scalars().first()

    async def _get_dishes_count(self, menu_id: int) -> int:
        dishes_count = await self.session.execute(
                select(func.count(Dish.id))
                .select_from(Submenu)
                .join(Submenu.dishes)
                .filter(Submenu.menu_id == menu_id)
        )
        return dishes_count.scalars().first()

    async def _get(self, menu_id: int) -> Menu | None:
        menu = await self.session.execute(
                select(Menu)
                .filter(Menu.id == menu_id)
                .options(selectinload(Menu.submenus)))
        menu = menu.scalars().first()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='menu not found')
        menu.submenus_count = await self._get_submenus_count(menu_id)
        menu.dishes_count = await self._get_dishes_count(menu_id)
        return menu
