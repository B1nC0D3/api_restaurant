from pydantic import BaseModel


class BaseItem(BaseModel):

    title: str
    description: str
