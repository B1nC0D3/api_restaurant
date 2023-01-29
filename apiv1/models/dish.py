from decimal import Decimal

from apiv1.models.base_models import BaseItem


class BaseDish(BaseItem):
    price: Decimal


class DishCreate(BaseDish):
    pass


class DishUpdate(BaseDish):
    pass


class DishResponse(BaseDish):
    id: str
    price: str

    class Config:
        orm_mode = True
