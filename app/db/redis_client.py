import json
from contextlib import asynccontextmanager
from typing import Annotated, Any, Optional

import redis.asyncio as redis
from fastapi import Depends

from app.core.enum.redis_db import RedisDB
from app.core.settings import settings


class RedisClient:
    """Упрощенный асинхронный Redis клиент"""

    def __init__(self, db: RedisDB):
        self._client = redis.from_url(
            str(settings.redis_url(db)), decode_responses=True, encoding="utf-8"
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self):
        await self._client.close()

    async def set_value(
        self, key: str, value: Any, expire: Optional[int] = None
    ):
        key = str(key)
        serialized = json.dumps(value, ensure_ascii=False)
        if expire:
            return await self._client.setex(key, expire, serialized)
        return await self._client.set(key, serialized)

    async def get_value(self, key: str) -> Optional[Any]:
        key = str(key)
        data = await self._client.get(key)
        if data is None:
            return None
        return json.loads(data)
