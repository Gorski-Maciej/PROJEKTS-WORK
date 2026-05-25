from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://postgres:cloudbudget@postgres:5432/cloudbudget"
    DUCKDB_PATH: str = "/data/cloudbudget.duckdb"
    REDIS_URL: str = "redis://redis:6379/0"
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672/"
    JWT_SECRET: str = Field(min_length=32)

    class Config:
        env_file = ".env"


settings = Settings()
