from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

from app.core.logger import logger

BASE_DIR = Path(__file__).parents[2]


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "app" / "core" / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "app" / "core" / "certs" / "public.pem"
    algorithm: str = "RS256"
    acces_token_expiration_minutes: int = 1500


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    # Project
    PROJECT_TITLE: str
    auth_jwt: AuthJWT = AuthJWT()

    # FastAPI
    FAST_API_PORT: int
    FAST_API_PREFIX: str = "/api"
    FAST_API_HOST: str = "0.0.0.0"

    # POSTGRES
    POSTGRES_HOST: str = "0.0.0.0"
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_HOST: str = "0.0.0.0"
    REDIS_PORT: int
    REDIS_PASSWORD: str

    OLLAMA_MODEL: str
    OLLAMA_HOST: str

    
    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=f"/{self.POSTGRES_DB}",
        )

    def redis_url(self, page) -> URL:
        """
        Assemble redis URL from settings.

        :return: redis URL.
        """
        return URL.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=int(self.REDIS_PORT),
            user=None,
            password=self.REDIS_PASSWORD,
            path=f"/{page}",
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
