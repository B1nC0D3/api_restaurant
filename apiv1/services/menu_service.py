from fastapi import Depends, status, HTTPException

from apiv1.models.menu import MenuResponse, MenuCreate, MenuUpdate
from database.db_operations.menu_cache import MenuCache
from database.db_operations.menu_operations import MenuOperations


class MenuService:

    def __init__(self, operations: MenuOperations = Depends(), cache: MenuCache = Depends()):
        self.operations = operations
        self.cache = cache

    async def get_menu(self, menu_id: int) -> MenuResponse:
        cache = await self.cache.get(menu_id)
        if cache:
            return cache
        menu = await self.operations.get(menu_id)
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='menu not found')
        menu = MenuResponse.from_orm(menu)
        await self.cache.set(menu_id, menu)
        return menu

    async def get_menus(self) -> list[MenuResponse]:
        menus = await self.operations.get_many()
        return menus

    async def create_menu(self, menu_data: MenuCreate) -> MenuResponse:
        menu = await self.operations.create(menu_data)
        menu = MenuResponse.from_orm(menu)
        await self.cache.set(int(menu.id), menu)
        return menu

    async def update_menu(self, menu_id: int, menu_data: MenuUpdate) -> MenuResponse:
        menu = await self.operations.update(menu_id, menu_data)
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='menu not found')
        menu = MenuResponse.from_orm(menu)
        await self.cache.set(menu_id, menu)
        return menu

    async def delete_menu(self, menu_id: int) -> None:
        await self.operations.delete(menu_id)
        await self.cache.delete(menu_id)
