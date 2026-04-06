import uuid
from typing import List, Optional

from sqlalchemy import UUID, Enum, String
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enum import UserRoleEnum
from app.db.postgresql.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String)
    surname: Mapped[str] = mapped_column(String)
    patronymic: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[BYTEA] = mapped_column(type_=BYTEA(1024))
    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum), nullable=False, default=UserRoleEnum.USER
    )

    session_games: Mapped[List["SessionGame"]] = relationship(
        "SessionGame", back_populates="user", cascade="all, delete-orphan"
    )
