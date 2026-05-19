from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./cloudbudget.db"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672//"
    REDIS_URL: str = "redis://localhost:6379/0"
    JWT_SECRET: str = "dev-secret"
    DUCKDB_PATH: str = "cloudbudget.duckdb"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()


# Backward-compatible aliases used by existing modules
Settings.database_url = property(lambda self: self.DATABASE_URL)
Settings.rabbitmq_url = property(lambda self: self.RABBITMQ_URL)
Settings.redis_url = property(lambda self: self.REDIS_URL)
Settings.jwt_secret = property(lambda self: self.JWT_SECRET)
Settings.duckdb_path = property(lambda self: self.DUCKDB_PATH)
