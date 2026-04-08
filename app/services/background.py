import json
from uuid import UUID

from app.core.enum.difficulty_level import DifficultyLevelEnum, get_prompt_user
from app.core.enum.redis_db import RedisDB
from app.db.postgresql.db import AsyncSession
from app.db.redis_client import RedisClient
from app.models.session_game.schemas import SessionGameRead
from app.models.user.schemas import UserRead
from app.services.session_game import SessionGameService
from app.utils.ai.ollama import OllamaChat
from app.utils.errors.error import CustomErrorCode, error_service


class BackgroundService:
    def __init__(
        self,
        ollama_chat: OllamaChat,
        session: AsyncSession,
    ):
        self.session = session
        self.ollama_chat = ollama_chat

    async def create(
        self,
        difficulty_level: DifficultyLevelEnum,
        session_game_id: UUID,
        current_user: UserRead,
    ) -> str:

        session_game: SessionGameRead = await SessionGameService(
            self.session
        ).get_by_id(session_game_id=session_game_id)

        if current_user.id == session_game.user_id:
            prompt = await get_prompt_user(
                full_name=session_game.full_name,
                difficulty_level=difficulty_level,
            )

            result = json.loads(await self.ollama_chat.generate(prompt))
            background = result.pop("background")

            await RedisClient(RedisDB.ROUND).set_value(
                key=session_game_id,
                value={
                    "background": background,
                    "rules": prompt,
                    "history": [],
                    "status": result,
                    "event": "",
                },
            )
            return {
                "background": background,
                "status": result,
            }

        raise error_service.error(
            CustomErrorCode.HTTP_403_FORBIDDEN,
            details=["Недостаточно прав"],
        )
