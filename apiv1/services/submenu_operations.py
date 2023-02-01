from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from apiv1.models.menu import SubmenuCreate, SubmenuUpdate
from apiv1.services.base import BaseService
from database.tables import Menu, Submenu


class SubmenuService(BaseService):

    async def get(self, menu_id: int, submenu_id: int) -> Submenu:
        return await self._get(menu_id, submenu_id)

    async def get_many(self, menu_id: int, user_id: int) -> list[Submenu]:
        submenus = await self.session.execute(select(Submenu)
                                              .filter(Submenu.menu_id == menu_id)
                                              .options(selectinload(Submenu.dishes)))
        submenus = submenus.unique().scalars().all()
        if submenus:
            await self._is_author(menu_id, user_id)
        return submenus

    async def create(self, menu_id: int, user_id: int, submenu_data: SubmenuCreate) -> Submenu:
        await self._check_menu_exists(menu_id)
        await self._is_author(menu_id, user_id)
        submenu = Submenu(**submenu_data.dict(), menu_id=menu_id)
        self.session.add(submenu)
        await self.session.commit()
        submenu = await self._get(menu_id, submenu.id)
        return submenu

    async def update(self, menu_id: int, submenu_id: int, user_id: int,
                     submenu_data: SubmenuUpdate) -> Submenu:
        submenu = await self._get(menu_id, submenu_id)
        await self._is_author(menu_id, user_id)
        for key, value in submenu_data:
            setattr(submenu, key, value)
        await self.session.commit()
        return submenu

    async def delete(self, menu_id: int, submenu_id: int, user_id: int) -> None:
        submenu = await self._get(menu_id, submenu_id)
        await self._is_author(menu_id, user_id)
        await self.session.delete(submenu)
        await self.session.commit()

    async def _get(self, menu_id: int, submenu_id: int) -> Submenu | None:
        submenu = await self.session.execute(
                select(Submenu)
                .filter(Submenu.id == submenu_id)
                .filter(Submenu.menu_id == menu_id)
        )
        submenu = submenu.scalars().first()
        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='submenu not found'
            )
        return submenu

    async def _check_menu_exists(self, menu_id: int):
        menu = await self.session.execute(select(Menu)
                                          .filter(Menu.id == menu_id))
        menu = menu.scalars().first()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='menu not found')

    async def _is_author(self, menu_id: int, user_id: int):
        menu = await self.session.execute(
                select(Menu)
                .filter(Menu.id == menu_id))
        if menu.user_id != user_id:
            raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='You are not the author')
