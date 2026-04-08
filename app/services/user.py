from typing import List

from app.core.enum import UserRoleEnum
from app.db.postgresql.db import AsyncSession
from app.models.user.repositories import UserRepository
from app.models.user.schemas import UserCreate, UserRead, UserUpdate
from app.utils.errors.error import CustomErrorCode, error_service


class UserService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def create(
        self,
        user: UserCreate,
    ) -> UserRead:
        return await UserRepository(self._session).create(**user.model_dump())

    async def get_by_filter_first(self, **kwargs) -> UserRead:
        result: UserRead = await UserRepository(self._session).get_by_filter_first(
            **kwargs
        )
        return result

    async def get_all(self) -> List[UserRead]:
        return await UserRepository(self._session).get_all()

    async def update(self, data: UserUpdate, user_id, current_user: UserRead):
        user: UserRead = await UserRepository(self._session).get_by_id(
            id=current_user.id
        )
        if user.role is UserRoleEnum.ADMIN or current_user.id == user_id:
            return await UserRepository(self._session).update_one(
                id=user_id, **data.dict(exclude_unset=True)
            )

        raise error_service.error(
            CustomErrorCode.HTTP_403_FORBIDDEN,
            details=["Недостаточно прав"],
        )

    async def delete(self, user_id, current_user: UserRead):
        user: UserRead = await UserRepository(self._session).get_by_id(
            id=current_user.id
        )
        if user.role is UserRoleEnum.ADMIN or current_user.id == user_id:
            return await UserRepository(self._session).delete_by_id(id=user_id)

        raise error_service.error(
            CustomErrorCode.HTTP_403_FORBIDDEN,
            details=["Недостаточно прав"],
        )
