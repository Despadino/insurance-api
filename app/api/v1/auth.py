from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Response

from app.api.middlewares.current_user import refresh_acess_token, validate_current_user
from app.api.middlewares.token import create_token, encode_jwt
from app.db.postgresql.db import AsyncSessionDep
from app.models.schemas.token import Token
from app.models.user.schemas import UserCreate, UserRead
from app.services.user import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)


@router.post(
    "/register",
    response_model=UserRead,
    summary="Регестрация нового пользователя",
)
async def register(
    user: UserCreate,
    session: AsyncSessionDep,
):
    user: UserRead = await UserService(session).create(
        user=user,
    )
    return user


@router.post("/login", response_model=Token)
async def login(response: Response, user: UserRead = Depends(validate_current_user)):
    jwt_payload = {"sub": str(user.id), "username": user.username}
    refresh_token = encode_jwt(
        payload=create_token("refresh", jwt_payload),
        expire_timedelta=timedelta(days=30),
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        expires=datetime.now(timezone.utc) + timedelta(days=30),
        httponly=True,
        secure=True,
    )

    access_token = encode_jwt(payload=create_token("access", jwt_payload))
    return Token(access_token=access_token)


@router.get("/refresh", response_model=Token)
async def refresh(token: Token = Depends(refresh_acess_token)):
    return token
