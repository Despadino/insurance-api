from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Path

from app.api.middlewares.current_user import CurrentUserDep
from app.api.middlewares.role_system import roles_required
from app.db.postgresql.db import AsyncSessionDep
from app.models.session_game.schemas import SessionGameCreate, SessionGameRead
from app.services.session_game import SessionGameService

router = APIRouter(
    prefix="/session_game",
    tags=["Управление играми"],
)


@router.post(
    "",
    response_model=SessionGameRead,
    summary="Создать игру",
    dependencies=[Depends(roles_required())],
)
async def endpoint(
    session: AsyncSessionDep,
    current_user: CurrentUserDep,
    data: SessionGameCreate,
):
    return await SessionGameService(session).create(
        data=data, current_user=current_user
    )


@router.delete(
    "/{sessionGameID}",
    summary="Удалить игру",
    dependencies=[Depends(roles_required())],
)
async def endpoint(
    session: AsyncSessionDep,
    current_user: CurrentUserDep,
    session_game_id: UUID = Path(alias="sessionGameID"),
):
    await SessionGameService(session).delete(
        session_game_id=session_game_id, current_user=current_user
    )
