from apiv1.models.base_models import BaseItem
from apiv1.models.dish import DishResponse


class SubmenuTask(BaseItem):
    id: str
    dishes: list[DishResponse | None]

    class Config:
        orm_mode = True


class MenuTask(BaseItem):
    id: str
    submenus: list[SubmenuTask | None]

    class Config:
        orm_mode = True
