import re

from pydantic import BaseModel, validator


class BaseUser(BaseModel):
    email: str
    username: str

    @validator('email')
    def validate_email(cls, v):
        if not re.match(r'^[-\w\.]+@[-\w\.]+\.\w{2,5}$', v):
            raise ValueError('Invalid email')
        return v


class UserCreate(BaseUser):
    password: str


class UserResponse(BaseUser):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
