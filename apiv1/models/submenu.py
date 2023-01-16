from .base import BaseItem


class SubmenuCreate(BaseItem):
    pass


class SubmenuUpdate(BaseItem):
    pass


class SubmenuResponse(BaseItem):

    id: str
    dishes_count: int

    class Config:
        orm_mode = True
