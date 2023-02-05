from fastapi import Depends
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apiv1.models.submenu import SubmenuCreate, SubmenuUpdate
from database.database import get_session
from database.db_operations.abstract_models import AbstractOperations
from database.tables import Menu, Submenu


class SubmenuOperations(AbstractOperations):
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get(self, menu_id: int, submenu_id: int) -> Submenu:
        async with self.session.begin():
            submenu = await self.session.execute(
                select(Submenu)
                .filter(Submenu.menu_id == menu_id)
                .filter(Submenu.id == submenu_id),
            )
        return submenu.scalars().first()

    async def get_many(self, menu_id: int) -> list[Submenu | None]:
        async with self.session.begin():
            submenus = await self.session.execute(
                select(Submenu).filter(Submenu.menu_id == menu_id),
            )
        return submenus.unique().scalars().all()

    async def create(self, menu_id: int, submenu_data: SubmenuCreate) -> Submenu | None:
        if not await self._check_menu_exists(menu_id):
            return None
        async with self.session.begin():
            submenu = await self.session.execute(
                insert(Submenu)
                .values(menu_id=menu_id, **submenu_data.dict())
                .returning(Submenu, Submenu.dishes_count),
            )
        return await self._submenu_data_to_model(submenu.first())

    async def update(
        self,
        menu_id: int,
        submenu_id: int,
        submenu_data: SubmenuUpdate,
    ) -> Submenu | None:
        async with self.session.begin():
            submenu = await self.session.execute(
                update(Submenu)
                .where(Submenu.menu_id == menu_id)
                .where(Submenu.id == submenu_id)
                .values(**submenu_data.dict())
                .returning(Submenu, Submenu.dishes_count),
            )
        return await self._submenu_data_to_model(submenu.first())

    async def delete(self, menu_id: int, submenu_id: int) -> int:
        async with self.session.begin():
            dishes_count = await self.session.execute(
                delete(Submenu)
                .where(Submenu.menu_id == menu_id)
                .where(Submenu.id == submenu_id)
                .returning(Submenu.dishes_count),
            )
        return dishes_count.first()[0]

    async def _check_menu_exists(self, menu_id: int) -> Menu:
        async with self.session.begin():
            menu = await self.session.execute(
                select(Menu).filter(Menu.id == menu_id),
            )
        return menu.scalars().first()

    async def _submenu_data_to_model(self, submenu_data: tuple) -> Submenu | None:
        if not submenu_data:
            return None
        submenu = Submenu(
            id=submenu_data[0],
            title=submenu_data[1],
            description=submenu_data[2],
            dishes_count=submenu_data[4],
        )
        return submenu
