import json
from typing import List, Optional
from uuid import UUID

from app.core.enum.difficulty_level import DifficultyLevelEnum, get_prompt_user
from app.core.enum.redis_db import RedisDB
from app.core.enum.round import get_random_incident
from app.core.logger import logger
from app.db.postgresql.db import AsyncSession
from app.db.redis_client import RedisClient, redis_client
from app.models.session_game.repositories import SessionGameRepository
from app.models.session_game.schemas import (
    SessionGameCreate,
    SessionGameRead,
    SessionGameUpdate,
)
from app.models.user.repositories import UserRepository
from app.models.user.schemas import UserRead
from app.services.session_game import SessionGameService
from app.utils.ai.ollama import OllamaChat
from app.utils.errors.error import CustomErrorCode, error_service


class RoundService:
    async def next_round(
        session_game_id: UUID,
    ):
        event = await get_random_incident()

        old_data = await RedisClient(RedisDB.ROUND).get_value(
            key=session_game_id,
        )
        old_data["event"] = event
        await RedisClient(RedisDB.ROUND).set_value(
            key=session_game_id,
            value=old_data,
        )

        return {
            "status": old_data["status"],
            "event": event,
        }

    async def finish_round(
        session: AsyncSession,
        current_user: UserRead,
        ollama_chat: OllamaChat,
        session_game_id: UUID,
        solving: str,
    ):
        old_data = await RedisClient(RedisDB.ROUND).get_value(
            key=session_game_id,
        )

        prompt = f"""
ознакомься:
правила которые были при сздании: {old_data["rules"]}
предыстория: {old_data.get("background")}
история персонажа: {old_data["history"]}

теперь я выдам тебе случай и решение
случай: {old_data["event"]}
решение: {solving}

текущий статус до событий (status): {old_data["status"]}

твоя задача вернуть актуальный status (повтори структуру 1в1 как передал)) но изменить статы смотря на то решение которое прислал. 
Управляй его финансами если annual_savings + то пользователь накапливает эту сумму а если - то каждый год уходит еще более большие долги

добавь новое поле report и опиши там правильно ли поступил пользователь или нет (желательно дать подсказку как можно было этого избежать и какая страховка бы помогла избежать этой проблемы)

если персонаж умер или дожил до 50 лет то ставь is_finish True. То в том случае пиши в report обобщение всей жизни и подведи итог. С акцентом на страхование
"""
        result = json.loads(await ollama_chat.generate(prompt))
        is_finish = result.get("is_finish")
        report = result.pop("report")
        old_data["history"].append(
            {
                "status": old_data["status"],
                "event": old_data["event"],
                "solving": solving,
                "report": report,
            }
        )
        old_data["status"] = result

        await RedisClient(RedisDB.ROUND).set_value(
            key=session_game_id,
            value=old_data,
        )

        if is_finish:
            data = await SessionGameService(session).finish(
                SessionGameUpdate(
                    id=session_game_id,
                    background=old_data["background"],
                    age=result.get("age"),
                    result=report,
                    is_finish=is_finish,
                ),
                #  current_user=current_user
            )

        return {"status": result, "report": report}
