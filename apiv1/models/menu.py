from decimal import Decimal

from pydantic import BaseModel


class BaseItem(BaseModel):
    title: str
    description: str


class BaseDish(BaseItem):
    price: Decimal


class DishCreate(BaseDish):
    pass


class DishUpdate(BaseDish):
    pass


class DishResponse(BaseDish):
    id: int
    price: str

    class Config:
        orm_mode = True


class SubmenuCreate(BaseItem):
    pass


class SubmenuUpdate(BaseItem):
    pass


class SubmenuResponse(BaseItem):
    id: int
    dishes: list[DishResponse]

    class Config:
        orm_mode = True


class MenuCreate(BaseItem):
    pass


class MenuUpdate(BaseItem):
    pass


class MenuResponse(BaseItem):
    id: int
    submenus: list[SubmenuResponse]

    class Config:
        orm_mode = True
