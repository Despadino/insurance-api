import asyncio
from typing import Annotated, Any, Dict, Optional

from fastapi import Depends, FastAPI, HTTPException
from ollama import AsyncClient
from pydantic import BaseModel

from app.core.settings import settings


class OllamaChat:
    def __init__(self, model: str):
        self.model = model
        self.client = AsyncClient(host=settings.OLLAMA_HOST)

    async def generate(self, prompt: str, **kwargs) -> str:
        messages = [{"role": "user", "content": prompt}]
        response = await self.client.chat(
            model=self.model, messages=messages, stream=False, options=kwargs
        )
        return response["message"]["content"]


_ollama_chat_instance = None
async def get_ollama_chat() -> OllamaChat:
    global _ollama_chat_instance
    if _ollama_chat_instance is None:
        _ollama_chat_instance = OllamaChat(model=settings.OLLAMA_MODEL)
    return _ollama_chat_instance

OllamaChatDep = Annotated[OllamaChat, Depends(get_ollama_chat)]
