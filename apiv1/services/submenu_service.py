from fastapi import Depends, HTTPException, status

from apiv1.models.submenu import SubmenuCreate, SubmenuResponse, SubmenuUpdate
from database.db_operations import menu_cache, submenu_cache
from database.db_operations.submenu_operations import SubmenuOperations
from database.tables import Submenu


class SubmenuService:
    def __init__(
        self, operations: SubmenuOperations = Depends(),
        sub_cache: submenu_cache.SubmenuCache = Depends(),
        m_cache: menu_cache.MenuCache = Depends(),
    ):
        self.operations = operations
        self.menu_cache = m_cache
        self.submenu_cache = sub_cache

    async def get_submenu(self, menu_id: int, submenu_id: int) -> SubmenuResponse:
        cache = await self.submenu_cache.get(submenu_id)
        if cache:
            return cache
        submenu = await self.operations.get(menu_id, submenu_id)
        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='submenu not found',
            )
        submenu = SubmenuResponse.from_orm(submenu)
        await self.submenu_cache.set(submenu_id, submenu)
        return submenu

    async def get_submenus(self, menu_id: int) -> list[Submenu]:
        return await self.operations.get_many(menu_id)

    async def create_submenu(self, menu_id: int, submenu_data: SubmenuCreate) -> SubmenuResponse:
        submenu = await self.operations.create(menu_id, submenu_data)
        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='menu not found',
            )
        submenu = SubmenuResponse.from_orm(submenu)
        await self.submenu_cache.set(int(submenu.id), submenu)
        await self.menu_cache.set_submenus_count(menu_id, 'add')
        return submenu

    async def update_submenu(
        self, menu_id: int,
        submenu_id: int, submenu_data: SubmenuUpdate,
    ) -> SubmenuResponse:
        submenu = await self.operations.update(menu_id, submenu_id, submenu_data)
        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='submenu not found',
            )
        submenu = SubmenuResponse.from_orm(submenu)
        await self.submenu_cache.set(submenu_id, submenu)
        return submenu

    async def delete_submenu(self, menu_id: int, submenu_id: int) -> None:
        dishes_count = await self.operations.delete(menu_id, submenu_id)
        await self.submenu_cache.delete(submenu_id)
        await self.menu_cache.set_submenus_count(menu_id, 'delete')
        for _ in range(dishes_count):
            await self.menu_cache.set_dishes_count(menu_id, 'delete')
