from uuid import UUID

from fastapi import APIRouter, Depends, Path

from app.api.middlewares.current_user import CurrentUserDep
from app.api.middlewares.role_system import roles_required
from app.core.enum import DifficultyLevelEnum
from app.db.postgresql.db import AsyncSessionDep
from app.services.round import RoundService
from app.utils.ai.ollama import OllamaChatDep

router = APIRouter(
    prefix="/round",
    tags=["Раунт игрока"],
)


@router.get(
    "/{sessionGameID}",
    # response_model=str,
    summary="Получить следующий раунт",
    dependencies=[Depends(roles_required())],
)
async def endpoint(
    session: AsyncSessionDep,
    # current_user: CurrentUserDep,
    session_game_id: UUID = Path(alias="sessionGameID"),
):
    return await RoundService.next_round(session_game_id=session_game_id)


@router.post(
    "/{sessionGameID}",
    # response_model=str,
    summary="Получить следующий раунт",
    dependencies=[Depends(roles_required())],
)
async def endpoint(
    solving: str,
    session: AsyncSessionDep,
    current_user: CurrentUserDep,
    ollama_chat: OllamaChatDep,
    session_game_id: UUID = Path(alias="sessionGameID"),

):
    return await RoundService.finish_round(
        session=session, current_user=current_user, solving=solving, session_game_id=session_game_id, ollama_chat=ollama_chat
    )
