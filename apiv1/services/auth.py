from datetime import datetime, timedelta

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy import select

from apiv1.models.auth import UserResponse, Token, UserCreate
from apiv1.services.base import BaseService
from database.tables import User
from settings import settings

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/sign-in')


async def get_current_user(token: str = Depends(oauth_scheme)) -> UserResponse:
    return await AuthService.validate_token(token)


class AuthService(BaseService):

    @classmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    async def hash_password(cls, plain_password: str) -> str:
        return bcrypt.hash(plain_password)

    @classmethod
    async def validate_token(cls, token: str) -> UserResponse:
        exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate credentials',
                headers={
                    'WWW-Authenticate': 'Bearer'
                }
        )
        try:
            payload = jwt.decode(
                    token,
                    settings.jwt_secret,
                    algorithms=[settings.jwt_algorithm]
            )
        except JWTError:
            raise exception

        user_data = payload.get('user')

        try:
            user = UserResponse.parse_obj(user_data)
        except ValidationError:
            raise exception

        return user

    @classmethod
    async def create_token(cls, user: User) -> Token:
        user_data = UserResponse.from_orm(user)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(days=settings.jwt_expiration),
            'sub': str(user_data.id),
            'user': user_data.dict()
        }
        token = jwt.encode(
                payload,
                settings.jwt_secret,
                algorithm=settings.jwt_algorithm
        )
        return Token(access_token=token)

    async def register_new_user(self, user_data: UserCreate) -> Token:
        user = User(
                email=user_data.email,
                username=user_data.username,
                password_hash=await self.hash_password(user_data.password)
        )
        self.session.add(user)
        await self.session.commit()

        return await self.create_token(user)

    async def authenticate_user(self, username: str, password: str) -> Token:
        exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate credentials',
                headers={
                    'WWW-Authenticate': 'Bearer'
                })
        user = await self.session.execute(
                select(User)
                .filter(User.username == username)
        )
        user = user.scalars().first()

        if not user:
            raise exception
        if not await self.verify_password(password, user.password_hash):
            raise exception
        return await self.create_token(user)
