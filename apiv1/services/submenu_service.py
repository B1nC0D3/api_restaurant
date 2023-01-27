from fastapi import Depends, HTTPException, status

from apiv1.models.submenu import SubmenuCreate, SubmenuResponse, SubmenuUpdate
from database.db_operations.submenu_operations import SubmenuOperations


class SubmenuService:
    def __init__(self, operations: SubmenuOperations = Depends()):
        self.operations = operations

    async def get_submenu(self, menu_id: int, submenu_id: int) -> SubmenuResponse:
        submenu = await self.operations.get(menu_id, submenu_id)
        print(submenu, '-----------------------------------')
        if not submenu:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='submenu not found')
        return submenu

    async def get_submenus(self, menu_id: int) -> list[SubmenuResponse]:
        return await self.operations.get_many(menu_id)

    async def create_submenu(self, menu_id: int, submenu_data: SubmenuCreate) -> SubmenuResponse:
        submenu = await self.operations.create(menu_id, submenu_data)
        if not submenu:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='menu not found')
        return submenu

    async def update_submenu(self, menu_id: int,
                             submenu_id: int, submenu_data: SubmenuUpdate) -> SubmenuResponse:
        submenu = await self.operations.update(menu_id, submenu_id, submenu_data)
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='submenu not found')
        return submenu

    async def delete_submenu(self, menu_id: int, submenu_id: int) -> None:
        await self.operations.delete(menu_id, submenu_id)
