from abc import ABC
from functools import wraps
from typing import Any, List

from sqlalchemy import delete, insert, inspect, select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.utils.errors.error import CustomErrorCode, error_service


def handle_repository_errors(func):
    """
    Декоратор для обработки ошибок в методах репозитория с привязкой к объекту
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except IntegrityError as e:
            error_str = str(e).lower()
            if "unique" in error_str or "duplicate" in error_str:
                logger.error(f"Нарушение уникальности для объекта: {str(e)}")
                raise error_service.error(CustomErrorCode.HTTP_409_CONFLICT)

        except Exception as e:
            logger.error(
                f"Неизвестная ошибка в БД {func.__name__} для объекта: {str(e)}"
            )
            raise error_service.error(CustomErrorCode.HTTP_500_INTERNAL_SERVER_ERROR)

    return wrapper


class AbstractRepository(ABC):
    def __init__(self, session: Session):
        self._session = session

    model = None

    async def commit(self):
        try:
            await self._session.commit()
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    def rollback(self):
        self._session.rollback()

    @handle_repository_errors
    async def get_by_id(self, id):
        return await self._session.get(self.model, id)

    @handle_repository_errors
    async def get_all(self) -> List[Any]:
        stmt = select(self.model)
        if hasattr(self.model, "order"):
            mapper = inspect(self.model)
            if "order" in mapper.columns:
                stmt = stmt.order_by(self.model.order.asc())
        result = await self._session.execute(stmt)
        return result.scalars().all()

    @handle_repository_errors
    async def create(self, **obj):
        query = insert(self.model).values(**obj).returning(self.model)
        result = await self._session.execute(query)
        return result.scalars().first()

    @handle_repository_errors
    async def update_one(self, id, **obj):
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**obj)
            .returning(self.model)
        )
        result = await self._session.execute(query)
        return result.scalars().first()

    @handle_repository_errors
    async def delete_by_id(self, id):
        result = await self._session.execute(
            delete(self.model).where(self.model.id == id)
        )
        return result.rowcount

    @handle_repository_errors
    async def get_by_filter(self, **kwargs) -> List[Any]:
        stmt = select(self.model).filter_by(**kwargs)
        mapper = inspect(self.model)
        if hasattr(mapper, "columns") and "order" in mapper.columns:
            stmt = stmt.order_by(self.model.order.asc())
        result = await self._session.execute(stmt)
        return result.scalars().all()

    @handle_repository_errors
    async def get_by_filter_first(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self._session.execute(query)
        return result.scalars().first()
