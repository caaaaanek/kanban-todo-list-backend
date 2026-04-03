from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_URL: str
    DATABASE_URL: str
    SECRET_KEY: str
    SESSION_EXPIRE_SECONDS: int = 86400
    CORS_ORIGINS: str

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"


settings = Settings()
