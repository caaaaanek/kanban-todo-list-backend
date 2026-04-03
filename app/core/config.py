from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_URL: str
    DATABASE_URL: str
    SECRET_KEY: str
    SESSION_EXPIRE_SECONDS: int = 86400

    class Config:
        env_file = ".env"


settings = Settings()
