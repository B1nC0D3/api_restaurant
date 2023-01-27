from fastapi import APIRouter, Depends, status

from apiv1.models.auth import UserResponse
from apiv1.models.menu import MenuCreate, MenuResponse, MenuUpdate
from apiv1.services.auth import get_current_user
from apiv1.services.menu_operations import MenuService

router = APIRouter(
    prefix='/menus')


@router.get('/', response_model=list[MenuResponse])
async def get_menus(menu_service: MenuService = Depends(),
                    user: UserResponse = Depends(get_current_user)):
    return await menu_service.get_many(user.id)


@router.get('/{menu_id}', response_model=MenuResponse)
async def get_menu(menu_id: int, menu_service: MenuService = Depends()):
    return await menu_service.get(menu_id)


@router.post('/', response_model=MenuResponse,
             status_code=status.HTTP_201_CREATED,)
async def create_menu(menu_data: MenuCreate, menu_service: MenuService = Depends(),
                      user: UserResponse = Depends(get_current_user)):
    return await menu_service.create(user.id, menu_data)


@router.patch('/{menu_id}', response_model=MenuResponse)
async def update_menu(menu_id: int, menu_data: MenuUpdate, menu_service: MenuService = Depends(),
                      user: UserResponse = Depends(get_current_user)):
    return await menu_service.update(menu_id, user.id, menu_data)


@router.delete('/{menu_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu(menu_id: int, menu_service: MenuService = Depends(),
                      user: UserResponse = Depends(get_current_user)):
    await menu_service.delete(menu_id, user.id)
