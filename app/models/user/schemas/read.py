from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from app.core.enum import UserRoleEnum


class Read(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,  
        populate_by_name=True,
    )

    id: UUID

    name: str
    surname: str
    patronymic: Optional[str] = None

    username: str
    role: UserRoleEnum

