from fastapi import APIRouter, Depends, status

from apiv1.models.dish import DishCreate, DishResponse, DishUpdate
from apiv1.services.dish_service import DishService

router = APIRouter(
    prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes')


@router.get('/', response_model=list[DishResponse])
async def get_dishes(menu_id: int, submenu_id: int,
                     dish_service: DishService = Depends()):
    return await dish_service.get_dishes(menu_id, submenu_id)


@router.get('/{dish_id}', response_model=DishResponse)
async def get_dish(menu_id: int, submenu_id: int,
                   dish_id: int, dish_service: DishService = Depends()):
    return await dish_service.get_dish(menu_id, submenu_id, dish_id)


@router.post('/', response_model=DishResponse,
             status_code=status.HTTP_201_CREATED)
async def create_dish(menu_id: int, submenu_id: int,
                dish_data: DishCreate, dish_service: DishService = Depends()):
    return await dish_service.create_dish(menu_id, submenu_id, dish_data)


@router.patch('/{dish_id}', response_model=DishResponse)
async def update_dish(menu_id: int, submenu_id: int, dish_id: int,
                dish_data: DishUpdate, dish_service: DishService = Depends()):
    return await dish_service.update_dish(menu_id, submenu_id, dish_id, dish_data)


@router.delete('/{dish_id}', status_code=status.HTTP_200_OK)
async def delete_dish(menu_id: int, submenu_id: int,
                dish_id: int, dish_service: DishService = Depends()):
    await dish_service.delete_dish(menu_id, submenu_id, dish_id)
    return {
        'status': True,
        'message': 'The dish has been deleted'
    }
