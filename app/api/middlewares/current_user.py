from fastapi import Depends, Form, Request
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer
from typing_extensions import Annotated

from app.api.middlewares.token import (
    create_token,
    decode_jwt,
    encode_jwt,
    validate_password,
)
from app.core.settings import settings
from app.db.postgresql.db import get_session
from app.models.schemas.token import Token
from app.models.user.repositories import UserRepository
from app.models.user.schemas import UserRead
from app.services.user import UserService
from app.utils.errors.error import CustomErrorCode, error_service


async def get_current_user(
    request: Request,
    access_token: HTTPAuthorizationCredentials = Depends(
        OAuth2PasswordBearer(tokenUrl=f"{settings.FAST_API_PREFIX}/v1/auth/login")
    ),
):
    decoded: dict = decode_jwt(access_token)
    if decoded.get("token_type") is None or decoded.get("token_type") != "access":
        raise error_service.error(CustomErrorCode.HTTP_403_FORBIDDEN)

    async for session in get_session():
        user: UserRead = await UserRepository(session).get_by_id(decoded["sub"])
        if not user:
            raise error_service.error(CustomErrorCode.HTTP_403_FORBIDDEN)

        user = UserRead.model_validate(user)

        request.state.current_user = user
        return user


async def validate_current_user(username: str = Form(), password: str = Form()):
    async for session in get_session():
        user = await UserService(session).get_by_filter_first(username=username)
        if not user or not validate_password(password, user.password):
            raise error_service.error(CustomErrorCode.HTTP_403_FORBIDDEN)
        return user


async def refresh_acess_token(request: Request):
    cookies = request.cookies
    refresh_token = cookies.get("refresh_token", None)
    if refresh_token is None:
        raise error_service.error(CustomErrorCode.HTTP_403_FORBIDDEN)

    decoded = decode_jwt(refresh_token)
    if decoded.get("token_type") is None or decoded.get("token_type") != "refresh":
        raise error_service.error(CustomErrorCode.HTTP_403_FORBIDDEN)

    async for session in get_session():
        user: UserRead = await UserRepository(session).get_by_id(decoded["sub"])
        if not user:
            raise error_service.error(CustomErrorCode.HTTP_403_FORBIDDEN)

        jwt_payload = {
            "sub": str(user.id),
            "username": user.username,
            "role": user.role,
        }
        access_token = encode_jwt(payload=create_token("access", jwt_payload))
        return Token(access_token=access_token)


async def get_current_user_request(request: Request):
    return request.state.current_user


CurrentUserDep = Annotated[UserRead, Depends(get_current_user_request)]
