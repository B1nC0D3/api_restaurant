from fastapi import APIRouter, Depends, status

from apiv1.models.menu import MenuCreate, MenuResponse, MenuUpdate
from apiv1.services.menu_operations import MenuService

router = APIRouter(
    prefix='/menus')


@router.get('/', response_model=list[MenuResponse])
def get_menus(menu_service: MenuService = Depends()):
    return menu_service.get_many()


@router.get('/{menu_id}', response_model=MenuResponse)
def get_menu(menu_id: int, menu_service: MenuService = Depends()):
    return menu_service.get(menu_id)


@router.post('/', response_model=MenuResponse,
             status_code=status.HTTP_201_CREATED)
def create_menu(menu_data: MenuCreate, menu_service: MenuService = Depends()):
    return menu_service.create(menu_data)


@router.patch('/{menu_id}', response_model=MenuResponse)
def update_menu(menu_id: int, menu_data: MenuUpdate, menu_service: MenuService = Depends()):
    return menu_service.update(menu_id, menu_data)


@router.delete('/{menu_id}', status_code=status.HTTP_200_OK)
def delete_menu(menu_id: int, menu_service: MenuService = Depends()):
    menu_service.delete(menu_id)
    return {
        'status': True,
        'message': 'The menu has been deleted'
    }
