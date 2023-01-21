from fastapi import HTTPException, status

from apiv1.models.submenu import SubmenuCreate, SubmenuUpdate
from database.tables import Dish, Submenu, Menu
from .base import BaseService


class SubmenuService(BaseService):

    def get(self, menu_id: int, submenu_id: int) -> Submenu:
        return self._get(menu_id, submenu_id)

    def get_many(self, menu_id: int) -> list[Submenu]:
        submenus = (
            self.session
            .query(Submenu)
            .filter(Submenu.menu_id == menu_id)
            .all()
        )
        for submenu in submenus:
            submenu.dishes_count = self._get_dishes_count(submenu.id)
        return submenus

    def create(self, menu_id: int, submenu_data: SubmenuCreate) -> Submenu:
        self._check_menu_exists(menu_id)
        submenu = Submenu(**submenu_data.dict(), menu_id=menu_id)
        self.session.add(submenu)
        self.session.commit()
        submenu.dishes_count = self._get_dishes_count(submenu.id)
        return submenu

    def update(self, menu_id: int, submenu_id: int,
               submenu_data: SubmenuUpdate) -> Submenu:
        submenu = self._get(menu_id, submenu_id)
        for key, value in submenu_data:
            setattr(submenu, key, value)
        self.session.commit()
        return submenu

    def delete(self, menu_id: int, submenu_id: int) -> None:
        submenu = self._get(menu_id, submenu_id)
        self.session.delete(submenu)
        self.session.commit()

    def _get(self, menu_id: int, submenu_id: int) -> Submenu | None:
        submenu = (
            self.session
            .query(Submenu)
            .filter(Submenu.menu_id == menu_id)
            .filter(Submenu.id == submenu_id)
            .first()
        )
        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='submenu not found'
            )
        submenu.dishes_count = self._get_dishes_count(submenu_id)
        return submenu

    def _get_dishes_count(self, submenu_id: int) -> int:
        result = (
            self.session
            .query(Dish)
            .select_from(Submenu)
            .join(Submenu.dishes)
            .filter(Submenu.id == submenu_id)
            .count()
        )
        return result

    def _check_menu_exists(self, menu_id: int):
        menu = (self.session
                .query(Menu)
                .filter(Menu.id == menu_id)
                .first()
                )
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='menu not found')
