from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Path

from app.api.middlewares.current_user import CurrentUserDep
from app.api.middlewares.role_system import roles_required
from app.core.enum import UserRoleEnum
from app.db.postgresql.db import AsyncSessionDep
from app.models.user.schemas import UserRead, UserUpdate
from app.services.user import UserService

router = APIRouter(
    prefix="/user",
    tags=["Пользователи"],
)


@router.get(
    "",
    response_model=List[UserRead],
    summary="Получить список пользователей",
    dependencies=[Depends(roles_required(UserRoleEnum.ADMIN))],
)
async def endpoint(session: AsyncSessionDep):
    return await UserService(session).get_all()


@router.get(
    "/me",
    response_model=UserRead,
    dependencies=[Depends(roles_required())],
    summary="Получить информацию текущего пользователя",
)
async def endpoint(current_user: CurrentUserDep):
    return current_user


@router.put(
    "/{userId}",
    summary="Обновить данные пользователя",
    dependencies=[Depends(roles_required())],
    response_model=UserRead,
)
async def endpoint(
    session: AsyncSessionDep,
    data: UserUpdate,
    current_user: CurrentUserDep,
    user_id: UUID = Path(alias="userId"),
):
    return await UserService(session).update(
        user_id=user_id, data=data, current_user=current_user
    )


@router.delete(
    "/{userId}",
    summary="Удаление пользователя",
    dependencies=[Depends(roles_required())],
)
async def endpoint(
    session: AsyncSessionDep,
    current_user: CurrentUserDep,
    user_id: UUID = Path(alias="userId"),
):
    await UserService(session).delete(user_id=user_id, current_user=current_user)
