from fastapi import Depends, status, HTTPException

from apiv1.models.menu import MenuResponse, MenuCreate, MenuUpdate
from database.db_operations.menu_operations import MenuOperations


class MenuService:
    def __init__(self, operations: MenuOperations = Depends()):
        self.operations = operations

    async def get_menu(self, menu_id: int) -> MenuResponse:
        menu = await self.operations.get(menu_id)
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='menu not found')
        return menu

    async def get_menus(self) -> list[MenuResponse]:
        menus = await self.operations.get_many()
        return menus

    async def create_menu(self, menu_data: MenuCreate) -> MenuResponse:
        menu = await self.operations.create(menu_data)
        return menu

    async def update_menu(self, menu_id: int, menu_data: MenuUpdate) -> MenuResponse:
        menu = await self.operations.update(menu_id, menu_data)
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='menu not found')
        return menu

    async def delete_menu(self, menu_id: int) -> None:
        await self.operations.delete(menu_id)
