from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_USER: str
    DB_NAME: str
    DB_PASS: str
    DB_HOST: str
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_MINUTES: int
    DB_HOST_ALEMBIC: str

    class Config:
        env_file = ".env"


settings = Settings()
