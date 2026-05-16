from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "CloudBudget API"
    api_prefix: str = "/api/v1"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./cloudbudget.db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    rabbitmq_url: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")
    duckdb_path: str = os.getenv("DUCKDB_PATH", "cloudbudget.duckdb")
    jwt_secret: str = os.getenv("JWT_SECRET", "dev-secret")


settings = Settings()
