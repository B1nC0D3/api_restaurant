from fastapi import Depends
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from apiv1.models.menu import MenuCreate, MenuUpdate
from database.database import get_session
from database.db_operations.abstract_models import AbstractOperations
from database.tables import Menu


class MenuOperations(AbstractOperations):
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get(self, menu_id: int) -> Menu:
        async with self.session.begin():
            menu = await self.session.execute(
                select(Menu).filter(Menu.id == menu_id),
            )
        return menu.scalars().first()

    async def get_many(self) -> list[Menu | None]:
        async with self.session.begin():
            menus = await self.session.execute(select(Menu))
        return menus.unique().scalars().all()

    async def create(self, menu_data: MenuCreate) -> Menu | None:
        async with self.session.begin():
            menu = await self.session.execute(
                insert(Menu)
                .values(**menu_data.dict())
                .returning(Menu, Menu.submenus_count, Menu.dishes_count),
            )
        return await self._menu_data_to_model(menu.first())

    async def update(self, menu_id: int, menu_data: MenuUpdate) -> Menu | None:
        async with self.session.begin():
            menu = await self.session.execute(
                update(Menu)
                .where(Menu.id == menu_id)
                .values(**menu_data.dict())
                .returning(Menu, Menu.submenus_count, Menu.dishes_count),
            )
        return await self._menu_data_to_model(menu.first())

    async def delete(self, menu_id: int) -> None:
        async with self.session.begin():
            await self.session.execute(
                delete(Menu).where(Menu.id == menu_id),
            )

    async def _menu_data_to_model(self, menu_data: tuple) -> Menu | None:
        if not menu_data:
            return None
        menu = Menu(
            id=menu_data[0],
            title=menu_data[1],
            description=menu_data[2],
            submenus_count=menu_data[3],
            dishes_count=menu_data[4],
        )
        return menu


class CeleryOperations:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_all_to_celery(self) -> list[Menu | None]:
        menus = await self.session.execute(
                select(Menu)
                .options(selectinload(Menu.submenus)))
        menus = menus.unique().scalars().all()
        return menus
