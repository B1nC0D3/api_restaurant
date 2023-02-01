from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from apiv1.models.menu import MenuCreate, MenuUpdate
from apiv1.services.base import BaseService
from database.tables import Menu, Submenu


class MenuService(BaseService):

    async def get(self, menu_id: int) -> Menu:
        return await self._get(menu_id)

    async def get_many(self, user_id: int) -> list[Menu]:
        menus = await self.session.execute(
                select(Menu)
                .filter(Menu.user_id == user_id)
                .options(selectinload(Menu.submenus)))
        menus = menus.unique().scalars().all()
        return menus

    async def create(self, user_id: int, menu_data: MenuCreate) -> Menu:
        menu = Menu(
            **menu_data.dict(),
            user_id=user_id
        )
        self.session.add(menu)
        await self.session.commit()
        menu = await self._get(menu.id)
        return menu

    async def update(self, menu_id: int, user_id: int, menu_data: MenuUpdate) -> Menu:
        menu = await self._get(menu_id)
        await self._is_author(user_id, menu.user_id)
        for key, value in menu_data:
            setattr(menu, key, value)
        await self.session.commit()
        return menu

    async def delete(self, menu_id: int, user_id: int) -> None:
        menu = await self._get(menu_id)
        await self._is_author(user_id, menu.user_id)
        await self.session.delete(menu)
        await self.session.commit()

    async def _get(self, menu_id: int) -> Menu | None:
        menu = await self.session.execute(
                select(Menu)
                .filter(Menu.id == menu_id)
                .options(selectinload(Menu.submenus, Submenu.dishes)))
        menu = menu.scalars().first()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='menu not found')
        return menu

    async def _is_author(self, user_id: int, author_id: int):
        if user_id != author_id:
            raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='You are not the author')
