from fastapi import APIRouter

from .routes import dishes, menus, submenus

router = APIRouter(
    prefix='/api/v1')

router.include_router(menus.router, tags=['menu'])
router.include_router(submenus.router, tags=['submenu'])
router.include_router(dishes.router, tags=['dish'])