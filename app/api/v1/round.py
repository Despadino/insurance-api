from uuid import UUID

from fastapi import APIRouter, Depends, Path

from app.api.middlewares.current_user import CurrentUserDep
from app.api.middlewares.role_system import roles_required
from app.db.postgresql.db import AsyncSessionDep
from app.models.schemas.game.get_event import GetEvent
from app.services.round import RoundService
from app.utils.ai.ollama import OllamaChatDep
from app.models.schemas.game.solving import Solving
from app.models.schemas.game.report import Report
router = APIRouter(
    prefix="/round",
    tags=["Раунт игрока"],
)


@router.get(
    "/{sessionGameID}",
    response_model=GetEvent,
    summary="Получить следующий раунт",
    dependencies=[Depends(roles_required())],
)
async def endpoint(
    session: AsyncSessionDep,
    current_user: CurrentUserDep,
    session_game_id: UUID = Path(alias="sessionGameID"),
):
    return await RoundService(session).next_round(
        current_user=current_user,
        session_game_id=session_game_id,
    )


@router.post(
    "/{sessionGameID}",
    response_model=Report,
    summary="Завершить раунд",
    dependencies=[Depends(roles_required())],
)
async def endpoint(
    solving: Solving,
    session: AsyncSessionDep,
    current_user: CurrentUserDep,
    ollama_chat: OllamaChatDep,
    session_game_id: UUID = Path(alias="sessionGameID"),
):
    return await RoundService(session).finish_round(
        current_user=current_user,
        solving=solving.solving,
        session_game_id=session_game_id,
        ollama_chat=ollama_chat,
    )
