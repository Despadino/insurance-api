from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class SqlalchemyBase(DeclarativeBase):
    """Base for all models."""

    metadata = sa.MetaData()


class Base(SqlalchemyBase):
    """Base for all models."""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
