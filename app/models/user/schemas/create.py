from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel

from app.api.middlewares.token import hash_password


class Create(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=to_camel, populate_by_name=True
    )
    name: str
    surname: str
    patronymic: Optional[str] = None

    username: str
    password: bytes = Field(
        ..., json_schema_extra={"type": "string", "format": "password"}
    )

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, v):
        return hash_password(v)
