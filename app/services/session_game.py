from typing import List, Optional
from uuid import UUID

from app.core.enum import UserRoleEnum
from app.core.logger import logger
from app.db.postgresql.db import AsyncSession
from app.models.session_game.repositories import SessionGameRepository
from app.models.session_game.schemas import (
    SessionGameCreate,
    SessionGameRead,
    SessionGameUpdate,
)
from app.models.user.repositories import UserRepository
from app.models.user.schemas import UserRead
from app.utils.errors.error import CustomErrorCode, error_service


class SessionGameService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_by_id(
        self,
        session_game_id: UUID,
    ) -> SessionGameRead:
        session_game: SessionGameRead = await SessionGameRepository(
            self.session
        ).get_by_id(id=session_game_id)

        if not session_game:
            raise error_service.error(
                CustomErrorCode.HTTP_404_NOT_FOUND,
                details=["Элемент не найден"],
            )
        return session_game

    async def create(
        self,
        data: SessionGameCreate,
        current_user: UserRead,
    ) -> SessionGameRead:
        return await SessionGameRepository(self.session).create(
            user_id=current_user.id, **data.model_dump()
        )

    async def finish(
        self,
        data: SessionGameUpdate,
        # current_user: UserRead,
    ) -> SessionGameRead:
        await SessionGameRepository(self.session).update_one(
            id=data.id,
            background=data.background,
            age=data.age,
            result=data.result,
            is_finish=data.is_finish,
        )

    async def delete(self, session_game_id: UUID, current_user: UserRead):

        session_game: SessionGameRead = await self.get_by_id(session_game_id)

        if (
            current_user.role is UserRoleEnum.ADMIN
            or current_user.id == session_game.user_id
        ):
            return await SessionGameRepository(self.session).delete_by_id(
                id=session_game_id
            )

        raise error_service.error(
            CustomErrorCode.HTTP_403_FORBIDDEN,
            details=["Недостаточно прав"],
        )
