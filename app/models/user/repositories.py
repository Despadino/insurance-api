from app.db.postgresql.abstract_repo import AbstractRepository

from .model import User


class UserRepository(AbstractRepository):
    model = User
