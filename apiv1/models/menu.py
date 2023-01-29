from apiv1.models.base_models import BaseItem


class MenuCreate(BaseItem):
    pass


class MenuUpdate(BaseItem):
    pass


class MenuResponse(BaseItem):
    id: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True
