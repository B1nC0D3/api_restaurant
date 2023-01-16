from fastapi import HTTPException, status

from apiv1.models.menu import MenuCreate, MenuUpdate
from database.tables import Dish, Menu, Submenu
from .base import BaseService


class MenuService(BaseService):

    def get(self, menu_id: int) -> Menu:
        return self._get(menu_id)

    def get_many(self) -> list[Menu]:
        menus = (
            self.session
            .query(Menu)
            .all()
        )
        for menu in menus:
            menu.submenus_count = self._get_submenus_count(menu.id)
            menu.dishes_count = self._get_dishes_count(menu.id)
        return menus

    def create(self, menu_data: MenuCreate) -> Menu:
        menu = Menu(
            **menu_data.dict()
        )
        self.session.add(menu)
        self.session.commit()
        menu.submenus_count = self._get_submenus_count(menu.id)
        menu.dishes_count = self._get_dishes_count(menu.id)
        return menu

    def update(self, menu_id: int, menu_data: MenuUpdate) -> Menu:
        menu = self._get(menu_id)
        for key, value in menu_data:
            setattr(menu, key, value)
        self.session.commit()
        return menu

    def delete(self, menu_id: int) -> None:
        menu = self._get(menu_id)
        self.session.delete(menu)
        self.session.commit()

    def _get_submenus_count(self, menu_id: int) -> int:
        result = (
            self.session
            .query(Submenu)
            .select_from(Menu)
            .join(Menu.submenus)
            .filter(Menu.id == menu_id)
            .count()
        )
        return result

    def _get_dishes_count(self, menu_id: int) -> int:
        result = (
            self.session
            .query(Dish)
            .select_from(Submenu)
            .join(Submenu.dishes)
            .filter(Submenu.menu_id == menu_id)
            .count()
        )
        return result

    def _get(self, menu_id: int) -> Menu | None:
        menu = (
            self.session
            .query(Menu)
            .filter(Menu.id == menu_id)
        ).first()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='menu not found')
        menu.submenus_count = self._get_submenus_count(menu_id)
        menu.dishes_count = self._get_dishes_count(menu_id)
        return menu
