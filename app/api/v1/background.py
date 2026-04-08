from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Path

from app.api.middlewares.current_user import CurrentUserDep
from app.api.middlewares.role_system import roles_required
from app.core.enum import DifficultyLevelEnum
from app.db.postgresql.db import AsyncSessionDep
from app.services.background import BackgroundService
from app.utils.ai.ollama import OllamaChatDep
from app.models.schemas.game.background import Background
router = APIRouter(
    prefix="/background",
    tags=["Предыстории игрока"],
)


@router.get(
    "/{difficultyLevel}/{sessionGameID}",
    response_model=Background,
    summary="Получить предысторию нового персонажа",
    dependencies=[Depends(roles_required())],
)
async def endpoint(
    session: AsyncSessionDep,
    ollama_chat: OllamaChatDep,
    current_user: CurrentUserDep,
    difficulty_level: Literal["EASY", "MEDIUM", "HARD"] = Path(alias="difficultyLevel"),
    session_game_id: UUID = Path(alias="sessionGameID"),
):
    return await BackgroundService(ollama_chat=ollama_chat, session=session).create(
        difficulty_level=DifficultyLevelEnum[difficulty_level],
        session_game_id=session_game_id,
        current_user=current_user,
    )
