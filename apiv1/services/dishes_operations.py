from fastapi import HTTPException, status

from apiv1.models.dish import DishCreate, DishUpdate
from database.tables import Dish
from .base import BaseService


class DishService(BaseService):

    def get(self, submenu_id: int, dish_id: int) -> Dish:
        return self._get(submenu_id, dish_id)

    def get_many(self, submenu_id: int) -> list[Dish]:
        dish = (
            self.session
            .query(Dish)
            .filter(Dish.submenu_id == submenu_id)
            .all()
        )
        return dish

    def create(self, submenu_id: int, dish_data: DishCreate) -> Dish:
        dish = Dish(**dish_data.dict(), submenu_id=submenu_id)
        self.session.add(dish)
        self.session.commit()
        return dish

    def update(self, submenu_id: int,
               dish_id: int, dish_data: DishUpdate) -> Dish:
        dish = self._get(submenu_id, dish_id)
        for key, value in dish_data:
            setattr(dish, key, value)
        self.session.commit()
        return dish

    def delete(self, submenu_id: int, dish_id: int) -> None:
        dish = self._get(submenu_id, dish_id)
        self.session.delete(dish)
        self.session.commit()

    def _get(self, submenu_id: int, dish_id: int) -> Dish | None:
        dish = (
            self.session
            .query(Dish)
            .filter(Dish.submenu_id == submenu_id)
            .filter(Dish.id == dish_id)
            .first()
        )
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='dish not found'
            )
        return dish
