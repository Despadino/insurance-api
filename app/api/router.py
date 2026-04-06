import asyncio

from fastapi import APIRouter

from .v1.auth import router as auth_router
from .v1.background import router as background_router
from .v1.round import router as round_router
from .v1.session_game import router as session_game_router
from .v1.user import router as user_router

api_router = APIRouter(prefix="/v1")

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(session_game_router)

api_router.include_router(background_router)
api_router.include_router(round_router)
