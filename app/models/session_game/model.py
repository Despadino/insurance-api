import uuid

from sqlalchemy import UUID, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.postgresql.base import Base


class SessionGame(Base):
    __tablename__ = "session_game"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)

    user_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("users.id", ondelete="CASCADE")
    )

    full_name: Mapped[str] = mapped_column(String)

    background: Mapped[str] = mapped_column(String, nullable=True)

    age: Mapped[int] = mapped_column(Integer, nullable=True, default=20)
    result: Mapped[str] = mapped_column(String, nullable=True)

    is_finish: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user: Mapped["User"] = relationship(back_populates="session_games")
