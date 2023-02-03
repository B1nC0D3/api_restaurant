from fastapi import APIRouter, Depends, status

from apiv1.models.menu import MenuCreate, MenuResponse, MenuUpdate
from apiv1.services.menu_service import MenuService

router = APIRouter(
    prefix="/menus",
)


@router.get("/", response_model=list[MenuResponse])
async def get_menus(menu_service: MenuService = Depends()):
    return await menu_service.get_menus()


@router.get("/{menu_id}", response_model=MenuResponse)
async def get_menu(menu_id: int, menu_service: MenuService = Depends()):
    return await menu_service.get_menu(menu_id)


@router.post(
    "/",
    response_model=MenuResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_menu(menu_data: MenuCreate, menu_service: MenuService = Depends()):
    return await menu_service.create_menu(menu_data)


@router.patch("/{menu_id}", response_model=MenuResponse)
async def update_menu(
    menu_id: int, menu_data: MenuUpdate, menu_service: MenuService = Depends()
):
    return await menu_service.update_menu(menu_id, menu_data)


@router.delete("/{menu_id}", status_code=status.HTTP_200_OK)
async def delete_menu(menu_id: int, menu_service: MenuService = Depends()):
    await menu_service.delete_menu(menu_id)
    return {
        "status": True,
        "message": "The menu has been deleted",
    }
