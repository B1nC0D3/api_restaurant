from fastapi import APIRouter, Depends, status

from apiv1.models.submenu import SubmenuCreate, SubmenuResponse, SubmenuUpdate
from apiv1.services.submenu_service import SubmenuService

router = APIRouter(
    prefix="/menus/{menu_id}/submenus",
)


@router.get("/", response_model=list[SubmenuResponse])
async def get_submenus(menu_id: int, submenu_service: SubmenuService = Depends()):
    return await submenu_service.get_submenus(menu_id)


@router.get("/{submenu_id}", response_model=SubmenuResponse)
async def get_submenu(
    menu_id: int, submenu_id: int, submenu_service: SubmenuService = Depends()
):
    return await submenu_service.get_submenu(menu_id, submenu_id)


@router.post(
    "/",
    response_model=SubmenuResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_submenu(
    menu_id: int,
    submenu_data: SubmenuCreate,
    submenu_service: SubmenuService = Depends(),
):
    return await submenu_service.create_submenu(menu_id, submenu_data)


@router.patch("/{submenu_id}", response_model=SubmenuResponse)
async def update_submenu(
    menu_id: int,
    submenu_id: int,
    submenu_data: SubmenuUpdate,
    submenu_service: SubmenuService = Depends(),
):
    return await submenu_service.update_submenu(menu_id, submenu_id, submenu_data)


@router.delete("/{submenu_id}", status_code=status.HTTP_200_OK)
async def delete_submenu(
    menu_id: int, submenu_id: int, submenu_service: SubmenuService = Depends()
):
    await submenu_service.delete_submenu(menu_id, submenu_id)
    return {
        "status": True,
        "message": "The submenu has been deleted",
    }
