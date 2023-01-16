from decimal import Decimal

from .base import BaseItem


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
