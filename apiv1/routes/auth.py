from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from apiv1.models.auth import UserCreate, Token
from apiv1.services.auth import AuthService

router = APIRouter(
        prefix='/auth'
)


@router.post('/sign-up', response_model=Token, status_code=status.HTTP_201_CREATED)
async def sign_up(user_data: UserCreate, auth_service: AuthService = Depends()):
    return await auth_service.register_new_user(user_data)


@router.post('/sign-in', response_model=Token)
async def sign_in(auth_data: OAuth2PasswordRequestForm = Depends(),
                  auth_service: AuthService = Depends()):
    return await auth_service.authenticate_user(auth_data.username, auth_data.password)
