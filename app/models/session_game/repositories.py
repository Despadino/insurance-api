from app.db.postgresql.abstract_repo import AbstractRepository

from .model import SessionGame


class SessionGameRepository(AbstractRepository):
    model = SessionGame
